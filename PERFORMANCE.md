```text
Document:    My Bloodborne Mac Performance Notes
Version:     v2.3.0
Author:      Christopher Celaya
Contact:     https://github.com/while-basic
Date:        2026-10-13
SHA256:      9850501e8966220329fe7e3c084616d301dda7f4166d8e87dd0e8a09de434d89
Chain:       solana-mainnet
Tx:          4yamfmzpSUm6yZbuPfY68LAw8mzYbzdtNmo4e7zgSszfwmNP5EWyW8xEaorGCrqnaTmp6wtBmvvbCaC3wXrr16hH
License:     The Unlicense (public domain dedication)
```

# Hunting the missing frames

My current baseline is **1080p / 60 FPS target / perf 3**. After a rough 900p
boss attempt, I went back to this setup and called the next run “very good.”
That describes how it felt. I did not collect new FPS or frame-time numbers
for that restored run.

```sh
python3 play.py --resolution 1080p --fps 60 --perf 3 --engine nightly \
  --fullscreen-mode borderless --present-mode Mailbox --vblank 60
```

The driver in that run fell back from Mailbox to Fifo. Asking for a present
mode does not prove the driver used it. I also enlarged the FPS text to 2.5
in shadPS4's local ImGui settings. Bigger numbers on screen do not make bigger
numbers in the game. I did not restore saves during the comparison.

## What I have seen so far

My shared footage shows 50+ FPS. Earlier play reports ranged from about 24–55,
with quieter spots near 60. These are scene-dependent results, not a steady
90+ FPS benchmark.

On October 12, I played with the DualShock while a script read the visible FPS
counter about once every one or two seconds. These are sampled counter values,
not a per-frame trace. The low column is a 10th percentile, not a 1% low.

| Profile and scene | Median FPS | 10th percentile | Min | Max |
| --- | ---: | ---: | ---: | ---: |
| 1080p / 60 cap / perf 3, carriage fight and gate | 47 | 43 | 37 | 60 |
| Same starting profile at 720p, bonfire mob | 53 | 48 | 37 | 60 |
| Default profile, crowded fight until death | 48 | 41 | 23 | 60 |

An older table also listed a perf-7 run with a median above its maximum. I
removed that row from the comparison because its summary is inconsistent.
The scenes above differ, so the table does not isolate resolution as the cause
of any gain. I need matching-route tests before making that claim.

Later that day:

| Attempt | What I reported | What I recorded |
| --- | --- | --- |
| 1080p before the change | Somewhat smooth | 212 seconds of activity counters |
| 900p / 60 cap / perf 3 at a boss | Extremely laggy | 234 seconds; 1600×900 buffers confirmed |
| Restored 1080p | Very good | 1920×1080 buffers and restored settings confirmed |

I removed the 900p resolution patch. Those recordings include travel and
loading, so I do not use their whole-run averages as a boss-only benchmark.
The recorder could not see the scene or detect my death.

## October 13: repeat tests beat wishful thinking

My first frame-by-frame test used the Central Yharnam lamp, facing the arched
door. I kept the character still. All four runs used the same local Release build,
1080p game image, 60 FPS++ patch, perf 3, and disabled Facegen. The window was
1280×720 logical pixels. Mailbox was requested; the driver used Fifo.

I changed only the emulated vblank rate between these runs. This controls
part of the emulator's frame timing. It is separate from the game's FPS cap.

| Run / vblank rate | Frames | Time | Average FPS | 1% low FPS | Slow-frame time (p99) |
| --- | ---: | ---: | ---: | ---: | ---: |
| First / 60 Hz | 2,148 | 59.95 s | 35.83 | 21.27 | 33.52 ms |
| First / 120 Hz | 2,718 | 59.98 s | 45.32 | 29.94 | 33.32 ms |
| Repeat / 120 Hz | 2,538 | 59.99 s | 42.31 | 20.91 | 41.69 ms |
| Return to 60 Hz | 2,549 | 59.95 s | 42.52 | 25.12 | 33.43 ms |

The first pair looked 26.5% faster at 120 Hz. The repeat did **not** back that up:
60 Hz and 120 Hz both averaged about 42 FPS. I am not claiming a vblank speedup
or changing the default. These ran on my active Mac; background load was not
held constant. Movement, game speed, sound, and combat also need checks.
The shared frame logger still needs an overhead check.
The [capture guide](docs/FRAME-CAPTURE.md) explains how I count frames and lows.

Two other trials did not earn a place in that table:

- A build with ThinLTO compiled and linked, then stalled before the game started.
  I rejected it and went back to the working Release build.
- A 90 FPS++ / 240 Hz trial reached gameplay, but the camera, character position,
  and window size changed during the capture. I kept the raw recording private
  and excluded it from the matching-scene comparison.

My 1080p / 60 cap / perf 3 working profile is still intact. A 90 FPS menu,
a higher cap, or one fast view does not meet my 90+ FPS gameplay goal.

The launcher's `--check` output now includes the requested vblank rate, window
mode, and present mode. A `null` present-mode request means to keep the current
setting; it does not mean the driver chose that mode. Vblank values outside
30–1000 Hz fail before any settings change. These checks do not run the game.

## A small buffer-pool bug

I found a stale GPU-progress check in shadPS4's command buffer pool. Even after
asking the GPU for fresh progress, the pool searched with the old value. It
could grow the pool when a ready buffer was waiting to be reused.

The [optional fix](patches/shadps4/resource-pool-refresh.patch) makes that search
use the refreshed value. A small check runs the real pool code with a test
clock. The old code fails both refresh cases. The fixed code passes all five
cases, including growing the pool when every buffer is still busy.

I built the fix and ran the same lamp view at 1080p, 60 cap, perf 3, and vblank
120. Across 2,482 frames in 59.97 seconds, it averaged **41.39 FPS**, with a
**23.94 FPS 1% low** and **41.73 ms p99 frame time**. That is near the repeated
baseline, so I do **not** claim an FPS gain. Walking and turning the camera
worked in a short check on a copied save. Combat, sound, and game speed still
need longer tests. See the [capture guide](docs/FRAME-CAPTURE.md) to try it.

## Fewer effects, higher cap

I also tried the original test build at 1080p with a 120 FPS++ cap, vblank 240,
and perf 7. That removes dynamic light shadows, SSAO, depth of field, and bloom
on top of the usual perf-3 changes. The picture changes, so this is a separate
quality tradeoff. It also changes three settings together.

The same still lamp view averaged **45.01 FPS** over 2,699 frames in 59.97
seconds. Its **1% low was 25.28 FPS** and **p99 frame time was 33.48 ms**. This
trial did not reach 90 FPS. I left the normal profile at perf 3.

## A buffer-write experiment

I tried widening a memory check for buffers to an aligned 16 KiB range. I kept
texture checks at their original size. The
[optional patch](patches/shadps4/buffer-write-window.patch) is off by default.
It checks that the whole range is mapped before widening anything.

These are three separate 60-second captures at the same Central Yharnam lamp,
facing the arched door. I kept 1080p, the 60 FPS++ cap, perf 3, vblank 120, and
the window size fixed. Each run used a fresh copy of the same starting save.

| Buffer experiment | Frames | Measured time | Average FPS | 1% low | p99 frame time | Worst frame |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| On, first run | 3,251 | 59.96 s | 54.22 | 28.67 | 33.21 ms | 47.91 ms |
| Off, same executable code | 2,277 | 59.98 s | 37.96 | 23.74 | 41.68 ms | 50.02 ms |
| On, repeat | 3,136 | 59.98 s | 52.29 | 23.97 | 33.37 ms | 141.44 ms |

The last two runs used the same command-line launch method. I checked the code
hash and the setting in each running process. The first run used the app bundle
launcher. Background work on my Mac was not held constant.

This is a promising gain in the average for this view. The repeat still had four
frames over 50 ms, including a 141 ms hitch. Its 1% low barely changed. It is
**not** a steady 90 FPS result, and this test still had a 60 FPS cap.

Ten checks pass against the actual changed methods. They cover mapped ranges,
gaps, address overflow, the off setting, and the unchanged texture range. I also
walked and turned the camera after the first capture. Those short checks looked
intact. They do not settle thread safety, busy routes, combat, sound, or game
speed. My normal 1080p profile is unchanged. The
[capture guide](docs/FRAME-CAPTURE.md#optional-buffer-write-experiment) explains
how to compare the patch with copied saves.

## Other paths I checked

- Exclusive fullscreen with the pool fix averaged **44.77 FPS**, with a
  **29.34 FPS 1% low**. I did not verify macOS Game Mode, so this is not a
  Game Mode result.
- Widening both buffer and texture checks averaged **38.88 FPS**. I rejected
  that broad version. It is not the patch shared above.
- Releasing a queue lock earlier averaged **42.37 FPS**. It showed no clear
  gain. A separate timing probe put the measured CPU submission steps below
  1% of each scheduler's time window. That does not measure GPU execution.

Each frame result above comes from a separate, still lamp-view capture of about
60 seconds at 1080p / cap 60 / perf 3 / vblank 120. These tests help narrow the
search. They do not replace a repeated busy gameplay route.

## What the code does, and where the time goes

This repo contains a Python launcher and a Mac activity recorder. The launcher
chooses patches and config, then starts shadPS4. It is not the game source or a
new renderer. My extracted `eboot.bin` is a PS4 x86-64 executable.

The investigated engine was **shadPS4 0.19.1 WIP**, commit
[`e0a4667`](https://github.com/shadps4-emu/shadPS4/commit/e0a466753a1aacbc8db8253be685bf7ab4d9daae),
using Rosetta and KosmicKrisp 26.2.99 on my M5 Max. GPU rendering was active.

That source accepts an ARM build target, but its
[`RunMainEntry`](https://github.com/shadps4-emu/shadPS4/blob/e0a466753a1aacbc8db8253be685bf7ab4d9daae/src/core/linker.cpp#L41-L64)
does not implement game entry outside x86-64. Compiling an ARM app alone will
not make the PS4 game run natively. Replacing the graphics layer would address
only part of that work.

A light 60-second follow-up capture showed these activity values:

| Counter | Median | Range |
| --- | ---: | ---: |
| Game main thread | 82.19% | 79.89–83.58% |
| GPU command thread | 69.61% | 67.97–76.43% |
| Rosetta exception thread | 48.69% | 46.66–51.45% |
| Whole-machine GPU use | 74% | 70–91% |

For a thread, 100% means one CPU core. GPU use includes other apps. These
counters show busy work, but they do not prove which stage limits frame rate.
The Rosetta exception work makes memory tracking worth studying. It does not
justify disabling memory protection or guessing at a fix.

## Keep the recorder light

```sh
python3 profile_runtime.py --seconds 3600 --interval 2 \
  --label "travel and boss attempt"
```

This reads thread and GPU activity. It does **not** read FPS, see the scene,
press buttons, change settings, or edit saves. Use `--pid` if more than one
emulator is running. Results stay in a new private `runtime/profiles/` folder.

For a long attempt, renew before the one-hour limit. Stop only the recorder
with Ctrl-C or SIGINT after the agreed stop point. It preserves samples and
marks an interrupted capture incomplete. Label menu, travel, combat, loading,
and death by direct observation or my report, not by a CPU graph.

I tried a heavy Metal System Trace during combat. It kept processing for
minutes, used about 16 GB of memory, and overlapped a report of major lag.
I stopped the profiler while leaving the game running. I exclude that period
from normal performance claims. **Do not repeat heavy tracing during combat.**
Some Apple stack-export tools also failed on this Rosetta process. Raw traces
can include private process data, so I keep them out of Git.

## The next useful test

I now have an [optional frame capture patch and analyzer](docs/FRAME-CAPTURE.md)
for a local emulator build. It captures real presentation intervals, while
the earlier recorder still measures CPU/GPU activity. Startup samples validate
the data path; they do not prove a gameplay speedup. Logger overhead still
needs a matching-scene comparison against an unmodified build.

1. Keep the working engine, config, patches, and saves backed up.
2. Choose the same busy location, camera, route, and warm shader cache.
3. Record real frame times or clearly label sampled on-screen FPS.
4. Repeat the baseline. Then change one thing and repeat the same route.
5. Compare slow frames, steady play, visual changes, and game speed.
6. Roll back any regression. Report unmeasured claims as unmeasured.

The working profile stays at 1080p. A lower-resolution trial, static view, or
higher FPS cap is a separate experiment. I have not delivered a native ARM
port, a renderer replacement, or verified steady 90+ FPS.
