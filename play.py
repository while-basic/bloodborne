#!/usr/bin/env python3
# Document:    Bloodborne launcher for bbport on Mac
# Version:     v2.0.0
# Author:      Christopher Celaya
# Contact:     https://github.com/while-basic
# Date:        2026-10-21
# SHA256:      92a866eeb422e51930bec867677994961a9ab0f74db8488a7e5ddabc410fd16b
# Chain:       solana-mainnet
# Tx:          66A3bqc9cnBKa3A24GVKKo1LMiWNzKv2mvYCidJ6rAtx4hu6z2XiyG8uamUCQ6M8R4RRMzXC5wSaVNpfeSH6i4d2
# License:     The Unlicense (public domain dedication)
"""Play my own Bloodborne copy with bbport for Mac.

The default is 1080p, a 60 FPS cap, perf 3, and fullscreen.
Install the pinned engine once with --install. Use --check to inspect the
local files without launching, and --stats for the last session's frame log.
A cap is a target, not a measured result.
"""
import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import urllib.request

ROOT = Path(__file__).resolve().parent
RUNTIME = ROOT / "runtime"
GAME = RUNTIME / "games/CUSA00900/eboot.bin"
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
# Keep preset numbers stable: levels 3 and 7 add no extra effect in bbport.
BBPORT_LADDER = [
    "Disable Motion Blur (perf increase)",
    "Disable Chromatic Aberration",
    None,
    "Disable Dynamic Light Shadows (perf increase)",
    "Disable SSAO",
    "Disable DoF",
    None,
]
SIZES = {"720p": (1280, 720), "900p": (1600, 900), "1080p": (1920, 1080), "1440p": (2560, 1440),
         "4k": (3840, 2160)}

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
    run = Path(args.bbport_src).expanduser() / "tools/macos/run.sh" if args.bbport_src else BBPORT_RUN
    if args.fps_size > 1 and not args.bbport_src:
        parser.error("--fps-size needs --bbport-src (the release bbport has no counter size setting).")
    if args.bbport_src and not (run.is_file() and (run.parents[2] / "out/bb-probe").is_file()):
        parser.error(f"No built bbport checkout at {args.bbport_src} (needs tools/macos/build.sh first).")
    if not run.is_file():
        parser.error("bbport is not installed yet. Run: python3 play.py --install")
    game_ready = (GAME_MERGED / "eboot.bin").is_file()
    sources_ready = GAME.is_file() and (GAME_PATCH / "eboot.bin").is_file()
    if not game_ready and not sources_ready:
        parser.error("Game files missing: supply the merged CUSA00900-109 folder, or both "
                     "CUSA00900 and CUSA00900-patch under runtime/games/. See README.md.")
    width, height = SIZES[args.resolution]
    patches = bbport_patches(args.perf, args.extra)
    if args.check:
        print(json.dumps({"engine": str(run), "resolution": args.resolution, "fps_target": args.fps,
                          "perf_level": args.perf, "patches": patches, "game": str(GAME_MERGED),
                          "game_ready": game_ready, "merge_needed": not game_ready, "data": str(BBPORT_DATA),
                          "fullscreen": args.fullscreen, "gameplay_verified": False}, indent=2))
        return 0
    if subprocess.run(["pgrep", "-x", "bb-probe"], stdout=subprocess.DEVNULL).returncode == 0:
        parser.error("Close the running game first.")
    merge_game()
    BBPORT_DATA.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, BB_DATA_DIR=str(BBPORT_DATA), BB_GAME_DIR=str(GAME_MERGED), BB_FPS=str(args.fps),
               BB_OUTPUT_RES=f"{width}x{height}", BB_RENDER_RES=f"{width}x{height}",
               BB_PATCHES=";".join(patches), BB_FULLSCREEN="1" if args.fullscreen else "0")
    env["BB_FPS_SCALE"] = str(args.fps_size)  # larger sizes need my optional overlay patch
    env["BB_SAVE_LOG"] = "0" if args.no_log else "1"
    build = f"own build {args.bbport_src}" if args.bbport_src else BBPORT_VERSION
    print(f"Launching bbport {build}: {args.resolution}, target {args.fps} FPS, perf level {args.perf}, "
          f"patches: {', '.join(patches) or 'none'}", flush=True)
    return subprocess.call(["bash", str(run)], cwd=ROOT, env=env)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--resolution", choices=SIZES, default="1080p")
    parser.add_argument("--fps", type=int, choices=(60, 90), default=60)
    parser.add_argument("--perf", type=int, choices=range(len(BBPORT_LADDER) + 1), default=3,
                        help="effects preset (0 = none; 3 = motion blur and color fringing off)")
    # Keep old bbport commands working; no other engine can be selected.
    parser.add_argument("--engine", choices=("bbport",), default="bbport", help=argparse.SUPPRESS)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--install", action="store_true", help="download and verify the pinned bbport release")
    action.add_argument("--stats", action="store_true", help="summarize the latest bbport frame CSV")
    action.add_argument("--check", action="store_true", help="check local files without changing or launching anything")
    parser.add_argument("--bbport-src", metavar="DIR", help="use your own built bbport-mac checkout")
    parser.add_argument("--fps-size", type=int, choices=range(1, 7), default=1, metavar="1-6",
                        help="with a patched --bbport-src build: make the FPS counter larger")
    parser.add_argument("--windowed", action="store_true", help="play in a window instead of fullscreen")
    parser.add_argument("--no-log", action="store_true", help="skip per-frame CSV recording (diagnostic logs remain)")
    parser.add_argument("--extra", action="append", default=[], metavar="PATCH_NAME",
                        help="enable an extra patch by its exact name in bbport's patch file (repeatable)")
    args = parser.parse_args()
    args.fullscreen = not args.windowed
    if args.install:
        install_bbport()
        return 0
    if args.stats:
        return bbport_stats(parser)
    return launch_bbport(args, parser)


if __name__ == "__main__":
    raise SystemExit(main())
