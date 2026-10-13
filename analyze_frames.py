#!/usr/bin/env python3
# Document:    My Bloodborne Frame Time Analyzer
# Version:     v1.0.0
# Author:      Christopher Celaya
# Contact:     https://github.com/while-basic
# Date:        2026-10-13
# SHA256:      86e4da960983087f82cdb07d6ce41d4e105c82b8fad4fa1ab9b77ccb9b244ba6
# Chain:       solana-mainnet
# Tx:          hoEZyRmMHqSxRCgGfvqvXybDBR4oJHqR9jXYExcYLgMjNunAhwW6NtCh7fcKRPnhK98pPStX9e3qzP9s1rBCwGS
# License:     The Unlicense (public domain dedication)
"""Summarize measured frame intervals from the optional shadPS4 capture patch.

This cannot identify gameplay, menus, loading, or a repeatable test route.
Select an observed interval with --start/--end and give it an honest --label.
"""

import argparse
import csv
import json
import math
from pathlib import Path
import statistics


def read_frames(path, start=0.0, end=None):
    if not math.isfinite(start) or start < 0:
        raise ValueError("Start must be a finite, nonnegative number")
    if end is not None and (not math.isfinite(end) or end <= start):
        raise ValueError("End must be finite and greater than start")
    frames = []
    previous = None
    with Path(path).open(newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != ["elapsed_seconds", "frame_ms"]:
            raise ValueError("Expected CSV columns: elapsed_seconds,frame_ms")
        for line, row in enumerate(reader, 2):
            try:
                if None in row or any(value is None for value in row.values()):
                    raise ValueError
                elapsed, duration = float(row["elapsed_seconds"]), float(row["frame_ms"])
            except (TypeError, ValueError) as error:
                raise ValueError(f"Invalid frame record on line {line}") from error
            if (not math.isfinite(elapsed) or not math.isfinite(duration)
                    or elapsed < 0 or duration <= 0):
                raise ValueError(f"Invalid frame timing on line {line}")
            if previous is not None and elapsed <= previous:
                raise ValueError(f"Timestamps must increase (line {line})")
            if previous is not None and not math.isclose(
                    (elapsed - previous) * 1000, duration, rel_tol=0.0001, abs_tol=0.001):
                raise ValueError(f"Missing frames or inconsistent duration (line {line})")
            previous = elapsed
            # Include only frames wholly inside the chosen observation window.
            if elapsed - duration / 1000 >= start and (end is None or elapsed <= end):
                frames.append((elapsed, duration))
    if not frames:
        raise ValueError("No complete frames in the selected interval")
    return frames


def percentile(sorted_values, fraction):
    position = (len(sorted_values) - 1) * fraction
    lo, hi = math.floor(position), math.ceil(position)
    return sorted_values[lo] + (sorted_values[hi] - sorted_values[lo]) * (position - lo)


def summarize(frames, label):
    durations = sorted(duration for _, duration in frames)
    total_ms = math.fsum(durations)
    slow_count = max(1, math.ceil(len(durations) * 0.01))
    return {
        "label": label,
        "scene_verified_by_tool": False,
        "source": "shadPS4 non-reused frame presentation intervals; not GPU execution time",
        "frames": len(durations),
        "measured_seconds": total_ms / 1000,
        "first_frame_start_seconds": frames[0][0] - frames[0][1] / 1000,
        "last_frame_end_seconds": frames[-1][0],
        "average_fps": len(durations) * 1000 / total_ms,
        "median_frame_ms": statistics.median(durations),
        "p95_frame_ms": percentile(durations, 0.95),
        "p99_frame_ms": percentile(durations, 0.99),
        "worst_frame_ms": durations[-1],
        "one_percent_low_fps": 1000 / statistics.mean(durations[-slow_count:]),
        "one_percent_low_method": "reciprocal of mean duration of the slowest ceil(N/100) frames",
        "fraction_within_90fps_budget": sum(t <= 1000 / 90 for t in durations) / len(durations),
        "frames_over_50ms": sum(t > 50 for t in durations),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path)
    parser.add_argument("--start", type=float, default=0)
    parser.add_argument("--end", type=float)
    parser.add_argument("--label", required=True, help="Observed scene and run; use 'unobserved' if unknown")
    args = parser.parse_args()
    if not args.label.strip():
        parser.error("Label must not be blank")
    try:
        result = summarize(read_frames(args.csv, args.start, args.end), args.label)
    except (OSError, ValueError, csv.Error) as error:
        parser.error(str(error))
    print(json.dumps(result, indent=2, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
