# Bloodborne on the M5 Max

```
Document:    Bloodborne on the M5 Max (shadPS4 launcher worktree)
Version:     v1.0.0
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-10-11
SHA256:      0567a2aa999e55c68d2f1ee5dc6ef1456e4abdeb0710e324f4d3664012060d74
Chain:       solana-mainnet
Tx:          2smTseJFkq5pV5Wb3AkQgLsLerhLTVbVbvarBAcvRiTc7aALwSFEopsNnAAMJ3QBPmJRBNPzWMKVGvwAMJ7ipGPF
License:     All Rights Reserved / Celaya Solutions
```

Personal, never billed. The game is the owner's own PS4 dump of Bloodborne (CUSA00900, v01.09).

## Launch

Double-click `Play Bloodborne.command`, or from a terminal:

```
python3 play.py                       # nightly engine, 1440p, 90 FPS target, windowed
python3 play.py --fullscreen          # borderless fullscreen
python3 play.py --resolution 1080p    # the agreed floor if 1440p/90 does not hold
python3 play.py --perf 2              # add cheaper visuals: 1 motion blur, 2 chromatic
                                      # aberration, 3 specific renders, 4 dynamic shadows
python3 play.py --check               # print the profile without launching
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

## Known limits

- shadPS4 for macOS is x86_64 and runs under Rosetta 2; the GPU path is KosmicKrisp
  (Vulkan on Metal). First visits to an area compile shaders synchronously and hitch.
- The 0.19.0 release crashed once in gameplay inside KosmicKrisp; the nightly is the default.
- Gameplay FPS at 1440p/90 has not been verified yet; title screen holds 90 FPS.
