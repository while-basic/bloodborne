#!/usr/bin/env python3
# Document:    Bloodborne launcher for shadPS4 on the M5 Max
# Version:     v1.5.1
# Author:      Christopher Celaya
# Contact:     https://github.com/while-basic
# Date:        2026-10-14
# SHA256:      e6d5583868f57eb821500f378614e4d397f84ff8198c935b0c879d60d51b3f41
# Chain:       solana-mainnet
# Tx:          4LiJQFfXWusGccp9ZfMDp8KzEwZkuvKLXLgtyF3wdfnRUQPHaLhsSjdSovK7AaybrrHhXFarGoEsPeg6cSpPgucq
# License:     The Unlicense (public domain dedication)
"""Launch the local Bloodborne copy with one explicit display profile.

The profile (resolution patch, FPS++ patch, performance patches) is installed into the
shadPS4 patches folder, so the Qt launcher applies the same profile as this script.

Defaults are 1080p / 60 FPS cap / perf 3 / borderless fullscreen with Facegen disabled.
Earlier M5 Max runs reached 57-60 FPS in quiet spots and about 41-48 in crowded
fights. The FPS option sets a target, not a measured result or a guaranteed floor.
See README.md and PERFORMANCE.md for the test context and current working profile.

--engine bbport runs bbport for Mac instead (install it once with --install). It held 56-59 FPS
where shadPS4 gave 43-48; --stats summarizes the last bbport session's frame log.
"""
import argparse
import copy
import csv
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
RUNTIME = ROOT / "runtime"
SHADPS4_HOME = Path.home() / "Library/Application Support/shadPS4"
ENGINES = {
    "nightly": Path.home() / "Library/Application Support/shadPS4QtLauncher/versions/Pre-release/shadps4",
    "release": RUNTIME / "Bloodborne Emulator.app/Contents/MacOS/shadps4",
    # Same nightly binary inside a bundle whose Info.plist declares a game category, so macOS Game Mode can engage.
    "nightly-app": RUNTIME / "Bloodborne Nightly.app/Contents/MacOS/shadps4",
}
GAME = RUNTIME / "games/CUSA00900/eboot.bin"
CONFIG = SHADPS4_HOME / "config.json"
PATCH_DIR = SHADPS4_HOME / "patches/bloodborne-profile"
# bbport for Mac (https://github.com/bmy/bbport-mac, GPL-2.0-or-later): a Bloodborne-only engine built
# on shadPS4's renderer. It loads the game without a full PS4 emulator, so less work sits between the
# game and the Mac. Everything it needs or writes stays under runtime/.
BBPORT_VERSION = "0.4-v1"
BBPORT_URL = f"https://github.com/bmy/bbport-mac/releases/download/{BBPORT_VERSION}/bbport-mac-{BBPORT_VERSION}.zip"
BBPORT_SHA256 = "61f4f44653b4eb6544b5c758529f51d4a997d93ef8b856318d47b2955ab23eac"
BBPORT_DIR = RUNTIME / f"engines/bbport-{BBPORT_VERSION}"
BBPORT_RUN = BBPORT_DIR / "bbport.app/Contents/Resources/bbport/tools/macos/run.sh"
BBPORT_DATA = RUNTIME / "bbport"
# bbport wants the base game and the 1.09 update merged into one folder.
GAME_PATCH = RUNTIME / "games/CUSA00900-patch"
GAME_MERGED = RUNTIME / "games/CUSA00900-109"
SHADPS4_SAVE = SHADPS4_HOME / "home/1000/savedata/CUSA00900/SPRJ0005"
# bbport's own copy of the community patch file uses these names; it has no Bloom or "lower renders" patch.
BBPORT_LADDER = [
    "Disable Motion Blur (perf increase)",
    "Disable Chromatic Aberration",
    None,
    "Disable Dynamic Light Shadows (perf increase)",
    "Disable SSAO",
    "Disable DoF",
    None,
]
TITLE_ID = "CUSA00900"
APP_VER = "01.09"
SIZES = {"720p": (1280, 720), "900p": (1600, 900), "1080p": (1920, 1080), "1440p": (2560, 1440),
         "4k": (3840, 2160)}
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


def selected_patches(resolution, fps, perf, extra=(), keep_facegen=False):
    selected = {"Skip Intro + warning message", "Performance Patch (Perf Increase)", f"{fps} FPS++"}
    if not keep_facegen:
        # Facegen "vertex explosions" (random spiky geometry on characters) hit twice on 2026-10-12.
        selected.add("Disable Facegen")
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
                         vblank_frequency=args.vblank, full_screen=args.fullscreen,
                         full_screen_mode=("Fullscreen" if args.fullscreen_mode == "exclusive"
                                           else "Fullscreen (Borderless)") if args.fullscreen else "Windowed")
    if args.present_mode:
        config["GPU"]["present_mode"] = args.present_mode
    # The resolution patches allocate bigger frame buffers; they need extra direct memory.
    config["General"].update(extra_dmem_in_mbytes=8192 if args.resolution == "4k" else 4096,
                             show_fps_counter=True)
    config["Vulkan"].update(pipeline_cache_enabled=True,
                             vkvalidation_core_enabled=bool(args.keep_vulkan_validation))
    config["Log"]["enable"] = not args.no_log
    config["Log"]["sync"] = False  # never block game threads on log writes
    temporary = CONFIG.with_suffix(".tmp")
    temporary.write_text(json.dumps(config, indent=2) + "\n")
    temporary.replace(CONFIG)
    return stamp


def bbport_patches(perf, extra=()):
    return [name for name in BBPORT_LADDER[:perf] if name] + list(extra)


def install_bbport():
    """Download the pinned bbport release, check its SHA-256, and unpack it under runtime/engines/."""
    if BBPORT_RUN.is_file():
        print(f"bbport {BBPORT_VERSION} is already installed: {BBPORT_DIR}")
        return
    downloads = RUNTIME / "downloads"
    downloads.mkdir(parents=True, exist_ok=True)
    archive = downloads / f"bbport-mac-{BBPORT_VERSION}.zip"
    if not archive.is_file():
        print(f"Downloading {BBPORT_URL}", flush=True)
        with urllib.request.urlopen(BBPORT_URL) as response, archive.open("wb") as out:
            shutil.copyfileobj(response, out)
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    if digest != BBPORT_SHA256:
        archive.unlink()
        raise RuntimeError(f"bbport download has the wrong SHA-256 ({digest}); deleted it, nothing installed.")
    with tempfile.TemporaryDirectory(dir=downloads) as scratch:
        # ditto keeps the app's code signature intact.
        subprocess.run(["ditto", "-x", "-k", str(archive), scratch], check=True)
        unpacked = next(Path(scratch).glob("*/bbport.app")).parent
        BBPORT_DIR.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(unpacked), BBPORT_DIR)
    print(f"Installed bbport {BBPORT_VERSION}: {BBPORT_DIR}")


def merge_game():
    """Make CUSA00900-109 (base game + 1.09 update) from APFS clones; the originals stay untouched."""
    if (GAME_MERGED / "eboot.bin").is_file():
        return
    if not (GAME_PATCH / "eboot.bin").is_file():
        raise RuntimeError(f"bbport needs the 1.09 update next to the game: {GAME_PATCH}")
    scratch = GAME_MERGED.with_name(GAME_MERGED.name + ".partial")
    shutil.rmtree(scratch, ignore_errors=True)
    subprocess.run(["cp", "-Rc", str(GAME.parent), str(scratch)], check=True)
    subprocess.run(["cp", "-Rc", f"{GAME_PATCH}/.", f"{scratch}/"], check=True)
    scratch.rename(GAME_MERGED)


def import_save():
    """Copy (never move) the shadPS4 save into bbport's layout the first time."""
    target = BBPORT_DATA / "user/savedata/1" / TITLE_ID / SHADPS4_SAVE.name
    if target.exists() or not SHADPS4_SAVE.is_dir():
        return None
    shutil.copytree(SHADPS4_SAVE, target, ignore=shutil.ignore_patterns("sce_sys"))
    return target


def frame_summary(rows, min_draws=500):
    """FPS summary of gameplay frames from a bbport frames CSV; menus and loading screens draw far less.
    Quitting can cut the last row short, so rows with missing fields are skipped."""
    times = sorted(float(row["frame_ms"]) for row in rows
                   if row.get("draws") and row.get("frame_ms")
                   and int(row["draws"]) >= min_draws and float(row["frame_ms"]) > 0)
    if not times:
        return None
    fps = [1000 / ms for ms in reversed(times)]  # slowest first
    slowest = times[-max(1, len(times) // 100):]
    return {"frames": len(fps), "median_fps": round(fps[len(fps) // 2], 1), "p10_fps": round(fps[len(fps) // 10], 1),
            "one_percent_low_fps": round(1000 * len(slowest) / sum(slowest), 1),
            "frames_under_58_fps_pct": round(100 * sum(f < 58 for f in fps) / len(fps), 1)}


def bbport_stats(parser):
    logs = sorted((BBPORT_DATA / "logs").glob("*.frames.csv"))
    if not logs:
        parser.error("No bbport frame log yet. Play once without --no-log first.")
    with logs[-1].open() as handle:
        summary = frame_summary(csv.DictReader(handle))
    print(json.dumps({"log": str(logs[-1]), "gameplay": summary}, indent=2))
    return 0


def launch_bbport(args, parser):
    if args.fps == 120:
        parser.error("bbport takes --fps 60 or 90.")
    if not BBPORT_RUN.is_file():
        parser.error("bbport is not installed yet. Run: python3 play.py --engine bbport --install")
    width, height = SIZES[args.resolution]
    patches = bbport_patches(args.perf, args.extra)
    if args.check:
        print(json.dumps({"engine": str(BBPORT_RUN), "resolution": args.resolution, "fps_target": args.fps,
                          "perf_level": args.perf, "patches": patches, "game": str(GAME_MERGED),
                          "game_ready": (GAME_MERGED / "eboot.bin").is_file(), "data": str(BBPORT_DATA),
                          "fullscreen": args.fullscreen, "gameplay_verified": False}, indent=2))
        return 0
    if subprocess.run(["pgrep", "-x", "bb-probe"], stdout=subprocess.DEVNULL).returncode == 0:
        parser.error("Close the running game first.")
    merge_game()
    imported = import_save()
    if imported:
        print(f"Copied your shadPS4 save to {imported}", flush=True)
    BBPORT_DATA.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, BB_DATA_DIR=str(BBPORT_DATA), BB_GAME_DIR=str(GAME_MERGED), BB_FPS=str(args.fps),
               BB_OUTPUT_RES=f"{width}x{height}", BB_RENDER_RES=f"{width}x{height}",
               BB_PATCHES=";".join(patches), BB_FULLSCREEN="1" if args.fullscreen else "0")
    if not args.no_log:
        env["BB_SAVE_LOG"] = "1"  # per-frame CSV in runtime/bbport/logs/
    print(f"Launching bbport {BBPORT_VERSION}: {args.resolution}, target {args.fps} FPS, perf level {args.perf}, "
          f"patches: {', '.join(patches) or 'none'}", flush=True)
    return subprocess.call(["bash", str(BBPORT_RUN)], cwd=ROOT, env=env)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--resolution", choices=SIZES, default="1080p")
    parser.add_argument("--fps", type=int, choices=(60, 90, 120), default=60)
    parser.add_argument("--perf", type=int, choices=range(len(PERF_LADDER) + 1), default=3,
                        help="performance patch ladder level (0 = base patches only; 3 = first three optional effects patches)")
    parser.add_argument("--engine", choices=[*ENGINES, "bbport"], default="nightly",
                        help="bbport = the Bloodborne-only engine from bbport-mac (install it with --install)")
    parser.add_argument("--install", action="store_true", help="with --engine bbport: download and check it")
    parser.add_argument("--stats", action="store_true", help="with --engine bbport: FPS summary of the last session")
    parser.add_argument("--windowed", action="store_true", help="run in a window instead of borderless fullscreen")
    parser.add_argument("--fullscreen-mode", choices=("borderless", "exclusive"), default="borderless",
                        help="borderless = SDL window over the desktop; exclusive = native macOS fullscreen space")
    parser.add_argument("--keep-facegen", action="store_true",
                        help="leave Facegen enabled (default disables it to stop the spiky-geometry glitch)")
    parser.add_argument("--vblank", type=int, default=None, metavar="HZ",
                        help="experimental emulated vblank rate, 30–1000 Hz; default = --fps. Measure changes before keeping them")
    parser.add_argument("--present-mode", choices=("Fifo", "Immediate", "Mailbox"), default=None,
                        help="swapchain present mode to request; support depends on the Vulkan driver")
    parser.add_argument("--no-log", action="store_true", help="disable the emulator log for a play session")
    parser.add_argument("--keep-vulkan-validation", action="store_true",
                        help="keep Vulkan core validation on for debugging; slower for play")
    parser.add_argument("--check", action="store_true", help="validate without changing settings or launching")
    parser.add_argument("--extra", action="append", default=[], metavar="PATCH_NAME",
                        help="also enable this patch by its exact XML name (repeatable)")
    args = parser.parse_args()
    args.vblank = args.fps if args.vblank is None else args.vblank
    if not 30 <= args.vblank <= 1000:
        parser.error("--vblank must be between 30 and 1000 Hz.")
    args.fullscreen = not args.windowed
    if args.engine == "bbport":
        if args.install:
            install_bbport()
            return 0
        if args.stats:
            return bbport_stats(parser)
        return launch_bbport(args, parser)
    emulator = ENGINES[args.engine]
    if args.engine == "nightly" and not emulator.is_file():
        emulator = ENGINES["release"]
    for path in (emulator, GAME, CONFIG, RUNTIME / "downloads/Bloodborne.xml"):
        if not path.is_file():
            parser.error(f"Required local file missing: {path}")
    profile, patches = make_profile(selected_patches(args.resolution, args.fps, args.perf, args.extra,
                                                     args.keep_facegen))
    if args.check:
        print(json.dumps({"engine": str(emulator), "resolution": args.resolution, "fps_target": args.fps,
                          "vblank_hz": args.vblank, "present_mode_requested": args.present_mode,
                          "vulkan_validation_core": args.keep_vulkan_validation,
                          "fullscreen_mode": args.fullscreen_mode if args.fullscreen else "windowed",
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
    print(f"Launching {args.engine} engine: {args.resolution}, target {args.fps} FPS, "
          f"vblank {args.vblank} Hz, perf level {args.perf}, "
          f"patches: {', '.join(patches)}", flush=True)
    print(f"Log: {log}", flush=True)
    env = dict(os.environ)
    # Exclusive fullscreen is a separate macOS Space; without this SDL hint the game minimizes whenever
    # another window takes focus, which also drops macOS Game Mode.
    env["SDL_VIDEO_MINIMIZE_ON_FOCUS_LOSS"] = "0"
    with log.open("w") as output:
        return subprocess.call([str(emulator), "--show-fps", "--game", str(GAME)], cwd=ROOT, env=env,
                               stdout=output, stderr=subprocess.STDOUT)


if __name__ == "__main__":
    sys.exit(main())
