```text
Document:    My Bloodborne Frame Capture Guide
Version:     v2.0.0
Author:      Christopher Celaya
Contact:     https://github.com/while-basic
Date:        2026-10-21
SHA256:      fd266e0e2ebd9f0d4013d11172e96fb46852c30131c3559ffc8a7bd183940fd3
Chain:       solana-mainnet
Tx:          5FWTMP9pNY6QGLEUqeq1ASFvsoUBGkH1hMLMHdhEQoPGyKt8JnxNb7Jzgq7TobXxtz3ovSK4FmMFUunpSDGCqSZt
License:     The Unlicense (public domain dedication)
```

# Count the frames that matter

bbport already records frame times. I use that recorder instead of adding a
second one. Back up saves and agree on the route and test length first.
A normal play session records a CSV unless you pass `--no-log`.

```sh
python3 play.py --resolution 1080p --fps 60 --perf 3
# Quit the game normally, then:
python3 play.py --stats
```

The CSVs live in `runtime/bbport/logs/`. `--stats` reads the latest one and
reports median FPS, the 10th percentile, a 1% low, and the share below 58 FPS.
The 1% low comes from the mean time of the slowest 1% of frames.
A partial final row from quitting is skipped.

The summary filters out rows with fewer than 500 draws. That removes many
menus and loading frames, but it is only a rough filter. It cannot recognize
combat, deaths, an empty room, or the same camera angle. `gameplay` in the JSON
means the filtered sample, not proof of a valid benchmark.

For a comparison, use the same scene, route, camera, resolution, effects,
power mode, and warm shader cache. Change one thing, repeat it, then repeat
the control. Record the bbport build, game version, display refresh, and any
visual problems. Check controls, sound, game speed, save/load, and crashes.

Keep first-visit stutter separate from repeat visits. A high cap, title screen,
short peak, or one smooth run does not prove steady 90+ FPS. Do not run heavy
tracing while measuring ordinary play. Raw captures and saves stay local.

My results and their limits are in [the performance notes](../PERFORMANCE.md).
