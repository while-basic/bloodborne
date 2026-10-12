#!/usr/bin/env python3
# Document:    Bloodborne launcher for shadPS4 on the M5 Max
# Version:     v1.1.0
# Author:      Celaya Solutions
# Contact:     hello@celayasolutions.com
# Date:        2026-10-11
# SHA256:      9e7adfc4300e1e08d11040b79f2322bb0355e884daeba4d9d8b617a7b092f534
# Chain:       solana-mainnet
# Tx:          61LqKnC5SrBxYBbzfyhUmM3B5NcmrVMQPDz2R9M2FsVmc8mxZ9nqrfppGxncW8GGebndCEeWqjP414kJYsS317ib
# License:     All Rights Reserved / Celaya Solutions
"""Launch the local Bloodborne copy with one explicit display profile.

The profile (resolution patch, FPS++ patch, performance patches) is installed into the
shadPS4 patches folder, so the Qt launcher applies the same profile as this script.
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
]


def selected_patches(resolution, fps, perf):
    selected = {"Skip Intro + warning message", "Performance Patch (Perf Increase)", f"{fps} FPS++"}
    if resolution != "1080p":
        width, height = SIZES[resolution]
        selected.add(f"Resolution Patch {width}x{height} (16:9)")
    selected.update(PERF_LADDER[:perf])
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
    parser.add_argument("--resolution", choices=SIZES, default="1440p")
    parser.add_argument("--fps", type=int, choices=(60, 90, 120), default=90)
    parser.add_argument("--perf", type=int, choices=range(len(PERF_LADDER) + 1), default=0,
                        help="performance patch ladder level (0 = Performance Patch only)")
    parser.add_argument("--engine", choices=ENGINES, default="nightly")
    parser.add_argument("--fullscreen", action="store_true", help="borderless fullscreen instead of a window")
    parser.add_argument("--no-log", action="store_true", help="disable the emulator log for a play session")
    parser.add_argument("--check", action="store_true", help="validate without changing settings or launching")
    args = parser.parse_args()
    emulator = ENGINES[args.engine]
    if args.engine == "nightly" and not emulator.is_file():
        emulator = ENGINES["release"]
    for path in (emulator, GAME, CONFIG, RUNTIME / "downloads/Bloodborne.xml"):
        if not path.is_file():
            parser.error(f"Required local file missing: {path}")
    profile, patches = make_profile(selected_patches(args.resolution, args.fps, args.perf))
    if args.check:
        print(json.dumps({"engine": str(emulator), "resolution": args.resolution, "fps_target": args.fps,
                          "perf_level": args.perf, "fullscreen": args.fullscreen, "patches": patches,
                          "profile_dir": str(PATCH_DIR), "gameplay_verified": False}, indent=2))
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
