```text
Document:    My Bloodborne Mac Performance Notes
Version:     v3.0.0
Author:      Christopher Celaya
Contact:     https://github.com/while-basic
Date:        2026-10-21
SHA256:      c05bbdbf931df0bc6c3d1950e2920f4f6f13fca4cf42923951f663d64dd39d68
Chain:       solana-mainnet
Tx:          2NWToGYERDJMnhS6tXseuSCSa2ASn62VcPuQFxKPcmMBokAHh6QKhoardh8pmXaeEnBKs6iTWFkm3PTa3y8Acjjt
License:     The Unlicense (public domain dedication)
```

# Hunting missing frames

This repo now uses bbport for Mac. My baseline is **1080p / 60 FPS cap /
perf 3 / fullscreen**. The goal is steady 60+ FPS in busy fights, then 90+.
Choosing a cap does not meet either goal.

## What I have seen with bbport

| When | What I checked | What happened |
| --- | --- | --- |
| October 13, 2026 | Central Yharnam, first lamp, 1080p / 60 cap, windowed | About 56–59 FPS |
| October 14, 2026 | My first crowd session | 60 FPS median, 60 FPS at the 10th percentile, about 9% of sampled frames below 58; some long hitches |

The crowd session felt smoother to me. It is one recorded session, not proof
of a floor through every fight. The summary uses a draw-count filter; it does
not recognize the scene by itself. I still need repeated matched crowd runs.
My earlier 50+ FPS footage reached more than a million people. That is my
report about the footage, not a new benchmark.

## What still needs checking

- Repeat the Central Yharnam crowd route with the same save, camera, and quality.
- Check controls, sound, game speed, picture quality, save/load, and longer play.
- Keep missing effects, pop-in, first-visit stutter, and crashes in the results.
- Test the optional vertex-format stand-in patch through a long fight.
- Verify the CSR names and loading label visually inside the game.
- Measure other Macs before making claims about them.

## How I measure

Use [bbport's frame log](docs/FRAME-CAPTURE.md), keep raw evidence private,
and record the engine build, game version, resolution, cap, effects, power
mode, and display refresh. Change one thing at a time and repeat the control.
A running process is not proof of gameplay. A higher cap is not more speed.

The older standalone-engine experiments are preserved in
[the pre-bbport-only history](https://github.com/while-basic/bloodborne/blob/bf3c96941a1b0b50583f9db5a8436d4081b8b236/PERFORMANCE.md).
Their results do not describe the current launcher. The old probes and
experimental patches are no longer part of the supported setup.

The October 21 launcher and mod checks ran locally. No new performance run
was done for that release, and I am not claiming a new FPS gain.
