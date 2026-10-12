#!/usr/bin/env python3
"""Passively record shadPS4 thread CPU and system-wide Apple GPU activity."""

import argparse
import ctypes
import ctypes.util
from datetime import datetime, timezone
import json
from pathlib import Path
import plistlib
import statistics
import subprocess
import sys
import time


class ThreadInfo(ctypes.Structure):
    _fields_ = [
        ("user_ns", ctypes.c_uint64), ("system_ns", ctypes.c_uint64),
        *[(name, ctypes.c_int32) for name in (
            "cpu_usage", "policy", "run_state", "flags", "sleep_time",
            "current_priority", "priority", "max_priority")],
        ("name", ctypes.c_char * 64),
    ]


def thread_snapshot(lib, pid):
    # PROC_PIDLISTTHREADS returns pthread handles, not numeric thread IDs.
    handles = (ctypes.c_uint64 * 4096)()
    size = lib.proc_pidinfo(pid, 6, 0, handles, ctypes.sizeof(handles))
    if size <= 0:
        raise OSError(ctypes.get_errno(), "Cannot read process threads")
    if size == ctypes.sizeof(handles):
        raise RuntimeError("Thread buffer is full; refusing an incomplete sample")
    result = {}
    for handle in handles[:size // 8]:
        info = ThreadInfo()
        # PROC_PIDTHREADINFO accepts the handles returned above (flavor 15 does not).
        read = lib.proc_pidinfo(pid, 5, handle, ctypes.byref(info), ctypes.sizeof(info))
        if read == ctypes.sizeof(info):
            result[str(handle)] = {
                "name": info.name.decode(errors="replace") or "(unnamed)",
                "cpu_time_ns": info.user_ns + info.system_ns,
            }
    if not result:
        raise RuntimeError("No thread counters available")
    return result


def gpu_snapshot():
    result = subprocess.run(
        ["ioreg", "-a", "-r", "-d", "1", "-c", "IOAccelerator"],
        capture_output=True, check=True, timeout=5,
    )
    devices = []
    for item in plistlib.loads(result.stdout):
        stats = item.get("PerformanceStatistics", {})
        if stats:
            devices.append({"model": item.get("model", "unknown"), **{
                key: value for key, value in stats.items()
                if "Utilization" in key
            }})
    if not devices:
        raise RuntimeError("No Apple GPU utilization counters available")
    return devices


def summarize(samples):
    threads = {}
    for sample in samples:
        for handle, row in sample["threads"].items():
            entry = threads.setdefault(handle, {"name": row["name"], "values": []})
            if row["cpu_percent"] is not None:
                entry["values"].append(row["cpu_percent"])
    ranked = []
    for handle, entry in threads.items():
        values = entry["values"]
        if values:
            ranked.append({"handle": handle, "name": entry["name"],
                           "median_cpu_percent": round(statistics.median(values), 2),
                           "max_cpu_percent": round(max(values), 2),
                           "sample_count": len(values)})
    return sorted(ranked, key=lambda row: row["median_cpu_percent"], reverse=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pid", type=int)
    parser.add_argument("--seconds", type=int, default=60)
    parser.add_argument("--interval", type=float, default=2)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--label", default="unconfirmed scene",
                        help="Human description of the scene or test phase")
    args = parser.parse_args()
    if sys.platform != "darwin":
        parser.error("This profiler requires macOS")
    if not 1 <= args.seconds <= 3600 or not 0.25 <= args.interval <= args.seconds:
        parser.error("Use 1–3600 seconds and an interval between 0.25 and the duration")
    if args.pid is None:
        matches = subprocess.run(["pgrep", "-x", "shadps4"], capture_output=True, text=True)
        pids = matches.stdout.split()
        if len(pids) != 1:
            parser.error("Expected one running shadps4 process; use --pid explicitly")
        args.pid = int(pids[0])
    if args.pid <= 0:
        parser.error("PID must be positive")
    lib = ctypes.CDLL(ctypes.util.find_library("proc"), use_errno=True)
    lib.proc_pidinfo.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_uint64,
                                ctypes.c_void_p, ctypes.c_int]
    lib.proc_pidinfo.restype = ctypes.c_int
    try:
        previous = thread_snapshot(lib, args.pid)
    except (OSError, RuntimeError) as error:
        parser.error(str(error))
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    output = args.output or Path(__file__).resolve().parent / "runtime/profiles" / stamp
    if output.exists():
        parser.error("Output directory already exists; choose a new one to preserve earlier samples")
    output.mkdir(parents=True)
    metadata = {"pid": args.pid, "started_utc": stamp, "duration_seconds": args.seconds,
                "interval_seconds": args.interval,
                "cpu_scope": "per thread; 100 percent equals one CPU core",
                "gpu_scope": "whole machine, includes other applications",
                "label": args.label, "scene": "not observed by this tool",
                "fps": "not measured by this tool"}
    (output / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    started = previous_time = time.monotonic()
    deadline = started + args.seconds
    samples = []
    failure = None
    print(f"Recording PID {args.pid} to {output}", flush=True)
    try:
        with (output / "samples.jsonl").open("x") as stream:
            while time.monotonic() < deadline:
                time.sleep(min(args.interval, max(0, deadline - time.monotonic())))
                current = thread_snapshot(lib, args.pid)
                now = time.monotonic()
                elapsed = now - previous_time
                rows = {}
                for handle, row in current.items():
                    old = previous.get(handle)
                    delta = (row["cpu_time_ns"] - old["cpu_time_ns"]
                             if old and old["name"] == row["name"] else -1)
                    rows[handle] = {**row, "cpu_percent":
                                    round(delta / elapsed / 1e7, 2) if delta >= 0 else None}
                sample = {"elapsed_seconds": round(now - started, 3),
                          "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                          "interval_seconds": elapsed, "threads": rows}
                try:
                    sample["gpu_system_wide"] = gpu_snapshot()
                except (OSError, RuntimeError, subprocess.SubprocessError, ValueError) as error:
                    sample["gpu_error"] = str(error)
                stream.write(json.dumps(sample) + "\n")
                stream.flush()
                samples.append(sample)
                hottest = sorted(rows.values(), key=lambda row: row["cpu_percent"] or 0,
                                 reverse=True)[:3]
                print(f"{sample['elapsed_seconds']:6.1f}s " + " | ".join(
                    f"{row['name']} {row['cpu_percent']}%" for row in hottest), flush=True)
                previous, previous_time = current, now
    except (OSError, RuntimeError, KeyboardInterrupt) as error:
        failure = str(error) or type(error).__name__
    summary = {"complete": failure is None, "error": failure, "samples": len(samples),
               "thread_cpu": summarize(samples), "gpu_scope": metadata["gpu_scope"]}
    (output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    if failure:
        print(f"Capture stopped: {failure}", file=sys.stderr)
    return 1 if failure else 0


if __name__ == "__main__":
    raise SystemExit(main())
