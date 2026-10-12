#!/usr/bin/env python3
# Document:    Bloodborne launcher for shadPS4 on the M5 Max
# Version:     v1.2.1
# Author:      Celaya Solutions
# Contact:     hello@celayasolutions.com
# Date:        2026-10-12
# SHA256:      a09711f2b47dd469d9953f007d831ed81d41e9a1d03be187bed395b79d015423
# Chain:       solana-devnet
# Tx:          5p6AfJGQiymFMefpmYaCFDYuu8GVgKVZAPMNWxnBVhD13Ktvcb4DrnGFg79kM8r7XKiFk7iKvB38xtSHTnL4pVeG
# License:     All Rights Reserved / Celaya Solutions
"""Launch the local Bloodborne copy with one explicit display profile.

The profile (resolution patch, FPS++ patch, performance patches) is installed into the
shadPS4 patches folder, so the Qt launcher applies the same profile as this script.

Defaults are 1080p / 60 FPS cap / perf 3 / fullscreen. Current owner-reported
gameplay is 24-55 FPS on an M5 Max with 128 GB unified memory. The FPS option
sets a target, not a measured result. See README.md for setup and limitations.
"""
import argparse
import copy
from datetime import datetime
import json
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
RUNTIME = ROOT / "runtime"
SHADPS4_HOME = Path.home() / "Library/Application Support/shadPS4"
ENGINES = {
    "nightly": Path.home() / "Library/Application Support/shadPS4QtLauncher/versions/Pre-release/shadps4",
    "release": RUNTIME / "Bloodborne Emulator.app/Contents/MacOS/shadps4",
}
GAME = RUNTIME / "games/CUSA00900/eboot.bin"
CONFIG = SHADPS4_HOME / "config.json"
PATCH_DIR = SHADPS4_HOME / "patches/bloodborne-profile"
TITLE_ID = "CUSA00900"
APP_VER = "01.09"
SIZES = {"1080p": (1920, 1080), "1440p": (2560, 1440), "4k": (3840, 2160)}
# Cumulative ladder: --perf N adds every entry up to N. Visual cost grows down the list.
PERF_LADDER = [
    "Disable Motion Blur (Perf Increase)",
    "Disable Chromatic Aberration",
    "lower specific renders (Perf Increase)",
    "Disable Dynamic Light Shadows (Perf Increase)",
    "Disable SSAO",
    "Disable DoF",
    "Disable Bloom",
]


def selected_patches(resolution, fps, perf, extra=()):
    selected = {"Skip Intro + warning message", "Performance Patch (Perf Increase)", f"{fps} FPS++"}
    if resolution != "1080p":
        width, height = SIZES[resolution]
        selected.add(f"Resolution Patch {width}x{height} (16:9)")
    selected.update(PERF_LADDER[:perf])
    selected.update(extra)
    return selected


def make_profile(selected):
    source = ET.parse(RUNTIME / "downloads/Bloodborne.xml").getroot()
    profile = ET.Element("Patch")
    profile.append(copy.deepcopy(source.find("TitleID")))
    found = set()
    for metadata in source.findall("Metadata"):
        if metadata.get("Name") in selected:
            if metadata.get("AppVer") != APP_VER:
                raise RuntimeError(f"Patch {metadata.get('Name')} is for game version {metadata.get('AppVer')}")
            element = copy.deepcopy(metadata)
            element.set("isEnabled", "true")
            profile.append(element)
            found.add(metadata.get("Name"))
    if found != selected:
        raise RuntimeError(f"Missing patches: {sorted(selected - found)}")
    return profile, sorted(found)


def install_profile(profile):
    """Write the profile where every shadPS4 engine auto-loads it (needs files.json)."""
    PATCH_DIR.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(profile).write(PATCH_DIR / f"{TITLE_ID}.xml", encoding="utf-8", xml_declaration=True)
    (PATCH_DIR / "files.json").write_text(json.dumps({f"{TITLE_ID}.xml": [TITLE_ID]}, indent=2) + "\n")


def write_config(args):
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    backups = RUNTIME / "config-backups"
    backups.mkdir(exist_ok=True)
    original = CONFIG.read_bytes()
    (backups / f"{stamp}.json").write_bytes(original)
    config = json.loads(original)
    width, height = SIZES[args.resolution]
    config["GPU"].update(internal_screen_width=width, internal_screen_height=height,
                         vblank_frequency=args.fps, full_screen=args.fullscreen,
                         full_screen_mode="Fullscreen (Borderless)" if args.fullscreen else "Windowed")
    # The resolution patches allocate bigger frame buffers; they need extra direct memory.
    config["General"].update(extra_dmem_in_mbytes=8192 if args.resolution == "4k" else 4096,
                             show_fps_counter=True)
    config["Vulkan"]["pipeline_cache_enabled"] = True
    config["Log"]["enable"] = not args.no_log
    config["Log"]["sync"] = False  # never block game threads on log writes
    temporary = CONFIG.with_suffix(".tmp")
    temporary.write_text(json.dumps(config, indent=2) + "\n")
    temporary.replace(CONFIG)
    return stamp


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--resolution", choices=SIZES, default="1080p")
    parser.add_argument("--fps", type=int, choices=(60, 90, 120), default=60)
    parser.add_argument("--perf", type=int, choices=range(len(PERF_LADDER) + 1), default=3,
                        help="performance patch ladder level (0 = base patches only; 3 = first three optional effects patches)")
    parser.add_argument("--engine", choices=ENGINES, default="nightly")
    parser.add_argument("--windowed", action="store_true", help="run in a window instead of borderless fullscreen")
    parser.add_argument("--no-log", action="store_true", help="disable the emulator log for a play session")
    parser.add_argument("--check", action="store_true", help="validate without changing settings or launching")
    parser.add_argument("--extra", action="append", default=[], metavar="PATCH_NAME",
                        help="also enable this patch by its exact XML name (repeatable)")
    args = parser.parse_args()
    args.fullscreen = not args.windowed
    emulator = ENGINES[args.engine]
    if args.engine == "nightly" and not emulator.is_file():
        emulator = ENGINES["release"]
    for path in (emulator, GAME, CONFIG, RUNTIME / "downloads/Bloodborne.xml"):
        if not path.is_file():
            parser.error(f"Required local file missing: {path}")
    profile, patches = make_profile(selected_patches(args.resolution, args.fps, args.perf, args.extra))
    if args.check:
        print(json.dumps({"engine": str(emulator), "resolution": args.resolution, "fps_target": args.fps,
                          "perf_level": args.perf, "fullscreen": args.fullscreen, "patches": patches,
                          "profile_dir": str(PATCH_DIR), "local_files_present": True,
                          "gameplay_verified": False}, indent=2))
        return 0
    if subprocess.run(["pgrep", "-x", "shadps4"], stdout=subprocess.DEVNULL).returncode == 0:
        parser.error("Close the running emulator before changing profiles.")
    stamp = write_config(args)
    install_profile(profile)
    logs = RUNTIME / "sessions"
    logs.mkdir(exist_ok=True)
    log = logs / f"{stamp}-{args.resolution}-{args.fps}-perf{args.perf}-{args.engine}.log"
    print(f"Launching {args.engine} engine: {args.resolution}, target {args.fps} FPS, perf level {args.perf}, "
          f"patches: {', '.join(patches)}", flush=True)
    print(f"Log: {log}", flush=True)
    with log.open("w") as output:
        return subprocess.call([str(emulator), "--show-fps", "--game", str(GAME)], cwd=ROOT,
                               stdout=output, stderr=subprocess.STDOUT)


if __name__ == "__main__":
    sys.exit(main())
