# Bloodborne on the M5 Max

```
Document:    Bloodborne on the M5 Max (shadPS4 launcher worktree)
Version:     v1.3.0
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-10-12
SHA256:      4a6935b1c0604c2ea9967a228baa5564f407dea1db1dba7911bb418f83c1ae79
Chain:       solana-mainnet
Tx:          27gxGHDwdjhRctJZHqbrF8WWzt2iyFMthvkw561hosM2zTbn8JVvBRMGw4kZ7nHx5ukVrH4sAh5a9Tv1Z1SPCkw9
License:     All Rights Reserved / Celaya Solutions
```

Personal, never billed. The game is the owner's own PS4 dump of Bloodborne (CUSA00900, v01.09).

## Launch

Double-click `Play Bloodborne.command`, or from a terminal:

```
python3 play.py                       # nightly engine, 1080p, 60 FPS cap, perf 3, fullscreen (measured best)
python3 play.py --resolution 1440p --fps 90 --perf 7   # sharper 2K profile, about 45 FPS in Yharnam
python3 play.py --windowed            # run in a window instead of borderless fullscreen
python3 play.py --perf 7              # cheaper visuals ladder: 1 motion blur, 2 chromatic aberration,
                                      # 3 specific renders, 4 dynamic shadows, 5 SSAO, 6 DoF, 7 bloom
python3 play.py --extra "Disable AA"  # any other patch by its exact name in Bloodborne.xml (repeatable)
python3 play.py --check               # print the profile without launching
python3 play.py --engine nightly-app --fullscreen-mode exclusive   # game-category bundle + native fullscreen Space:
                                      # the only combination where macOS Game Mode engages (see notes: glitch seen once)
python3 play.py --resolution 720p     # 720p / 900p exist for diagnostics (GPU-bound vs CPU-bound tests)
python3 play.py --vblank 240          # emulated vblank above the FPS++ cap (pacing test; default = --fps)
python3 play.py --present-mode Fifo   # KosmicKrisp only offers the Fifo family; a Mailbox request falls back to Fifo
```

The script backs up `config.json`, sets the internal resolution and vblank rate, installs the
patch profile into `~/Library/Application Support/shadPS4/patches/bloodborne-profile/` (with
the `files.json` index every engine needs to auto-load it), then starts the emulator with the
FPS overlay on. Because the profile lives in the patches folder, the Qt launcher
(`/Applications/shadPS4QtLauncher.app`) applies the same profile.

## Layout

`runtime/` is gitignored (about 36 GB): extracted game and update, the 0.19.0 app bundle,
`downloads/Bloodborne.xml` (upstream patch set), `sessions/` logs, `config-backups/`, and
`evidence-20261011/` (the laggy session log, the 0.19.0 crash report, a save backup).

## Measured (2026-10-12, Central Yharnam rooftops, scripted 60 s walk, FPS overlay read by OCR)

| Profile (nightly engine unless noted)            | median | p10 | min | max |
|--------------------------------------------------|-------:|----:|----:|----:|
| 1440p, 90 cap, perf 0, windowed                   | 34 | 31 | 29 | 46 |
| 1440p, 90 cap, perf 4                             | 40 | 35 | 34 | 50 |
| 1440p, 90 cap, perf 7                             | 45 | 39 | 38 | 53 |
| 1440p, 90 cap, perf 7 + 1440p Light Grid          | 45 | 40 | 37 | 59 |
| 1440p, 90 cap, perf 7 + Disable AA + Model LOD 2  | 49 | 44 | 42 | 61 |
| 1080p, 90 cap, perf 0                             | 60 | 54 | 51 | 69 |
| 1080p, 90 cap, perf 7                             | 55 | 47 | 43 | 68 |
| 1080p, 60 cap, perf 3, windowed                   | 54 | 48 | 43 | 60 |
| 1080p, 60 cap, perf 3, 0.19.0 release             | 53 | 42 | 18 | 60 |
| **1080p, 60 cap, perf 3, fullscreen (default)**   | **57** | **54** | **44** | **60** |

Indoors (Iosefka's Clinic) 1440p/90 ran about 54. While the owner played with the DualShock
at 1440p/90 the overlay sat at 37 (28 to 42). Reading: 1440p is pixel-bound in the Vulkan-on-
Metal path (1080p nearly doubles it); at 1080p the limit moves to CPU-side emulation under
Rosetta (cheaper effects stop helping), so 90 FPS is out of reach at any resolution on this
emulator build. Run-to-run noise is about +/-5 because the character drifts a little each run.

## Measured again (2026-10-12, live play with the DualShock, FPS overlay read by OCR every ~1-2 s)

| Run | Profile | Scene | median | p10 | min | max |
|-----|---------|-------|-------:|----:|----:|----:|
| r0 | default (1080p, 60 cap, perf 3, borderless) | carriage fight + gate vista | 47 | 43 | 37 | 60 |
| r1 | same at **720p** internal | bonfire mob | 53 | 48 | 37 | 60 |
| r4 | default via the game-category bundle, borderless | gate vista + fights | 45 | 39 | 32 | 49 |
| r5c | perf 7 + Model LOD 1 + 1080p Light Grid | gate vista, standing | 45 (51 standing) | 43 | 43 | 49 |
| r7b | default | crowded fight to death | 48 | 41 | 23 | 60 |

What the numbers mean: the hottest emulator thread sits at 77-90% of one core in every run (the
game's own x86-64 code under Rosetta); halving the pixels (720p) adds ~6 FPS and the draw-call
patches add ~3-8 at a static spot while relieving only the second thread (shadPS4's GPU command
processor, 72-75% -> 63%). 60 FPS held in crowds is therefore not reachable on this emulator path;
the crowd floor is ~41 FPS at 1080p. macOS Game Mode engages only for the bundle in exclusive
fullscreen, and that window vanishes when another app takes focus, so it is not usable yet.
Facegen vertex explosions (spiky geometry) appeared twice; `Disable Facegen` is now in the default
profile (`--keep-facegen` restores it).

## Known limits

- shadPS4 for macOS is x86_64 and runs under Rosetta 2; the GPU path is KosmicKrisp
  (Vulkan on Metal). First visits to an area compile shaders synchronously and hitch.
- The 0.19.0 release crashed once in gameplay inside KosmicKrisp and keeps its own shader
  cache (186 compiles on a warm area); the nightly is the default.
- The 2K at 90 goal is not reachable yet; see the table. Re-measure after emulator or
  driver updates with the scratch helpers described in the project notes.
- Once in a while a process stops taking keyboard input (seen after the DualShock dropped
  its Bluetooth link); restarting the game fixes it.
- A loading screen froze once after the game sat idle at the title for six hours
  (GPU thread idle, game threads waiting); restart and continue.
