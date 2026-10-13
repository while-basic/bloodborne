```text
Document:    My Bloodborne Mac Performance Notes
Version:     v2.6.0
Author:      Christopher Celaya
Contact:     https://github.com/while-basic
Date:        2026-10-13
SHA256:      6769ad988c452f9a1cc1e1bb6f8d349b432d357c94c5dcd0d9ef1ff8dd97bc91
Chain:       solana-mainnet
Tx:          oVyWzvZj36eRuTSVMym2QoUUvYPTRXi3LMxbSBE3J2vrtMKzojnN8cLPC3cYFDZVnW5QkZibT2SeqS91kvZemmq
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

## Bigger buffer groups

I added 64 and 256 KiB choices to the optional patch. I also fixed a boundary
case: a wider group must cover the whole original request. A request that
crosses the group keeps its original size.

These later tests use one executable, 1080p, a 120 FPS++ cap, perf 3, and vblank
120. The requested Mailbox display mode falls back to Fifo on this driver.
Each capture covers 60 seconds at the same still lamp view, with copied saves.
The private renderer timer and thread-priority experiments were off.

| Buffer group | Average FPS | 1% low | Worst frame |
| --- | ---: | ---: | ---: |
| 16 KiB | 45.85 | 29.94 | 33.71 ms |
| 64 KiB | 55.17 | 35.75 | 33.72 ms |
| 256 KiB | 49.89 | 26.25 | 66.59 ms |
| 16 KiB, fresh repeat | 39.76 | 7.66 | 173.37 ms |
| 16 KiB, later window in that repeat | 45.52 | 11.67 | 1,025.64 ms |
| 64 KiB, fresh repeat | 56.36 | 29.67 | 45.44 ms |

The 64 KiB average repeated well. The 16 KiB repeats were uneven, and I did
not hold background work constant. I requested window focus before the later
16 KiB capture, but did not measure focus through the run. These results do
not prove that the group size alone caused the gain. I kept a manually moved
trial out of this comparison.

I also tried Immediate display mode with 64 KiB. It averaged **53.06 FPS**,
with a **21.66 FPS 1% low** and an **83.30 ms** worst frame. That was no clear
win. I have not checked tearing or sound in that mode.

With 64 KiB and the usual display mode, raising vblank from 120 to 240 averaged
**56.49 FPS**, with a **29.46 FPS 1% low** and a **41.56 ms** worst frame.
That is almost the same average as the 120-vblank repeat. A faster timer did
not get me to 90 FPS.

The updated patch passes 40 memory checks and 14 setting checks. It stays
off by default. These still views do not verify combat, game speed, or steady
90+ FPS. My normal profile stays unchanged.

## Driver tables: the repeat gets the last word

I built a private Mesa driver that can reuse unchanged descriptor tables.
These tables tell the GPU where to find its data. The switch is off by default.
Thirty checks passed against the changed methods, including reset handling.

I used one driver and executable for these 60-second lamp-view captures.
They kept 1080p, cap 120, perf 3, vblank 120, and the 64 KiB buffer experiment.
The other timing probes and thread-priority experiment were off.

| Reuse tables | Average FPS | 1% low | Worst frame |
| --- | ---: | ---: | ---: |
| Off, first | 27.63 | 12.75 | 100.02 ms |
| On | 50.74 | 20.71 | 100.01 ms |
| Off, repeat | 54.77 | 27.72 | 42.35 ms |

The first pair looked like a win. The repeat took that win away. I have not
shown a gain from this change, so I kept it private and left reuse off.
Background work and window focus were not held constant through each run.

With that same driver and reuse off, I tried fewer effects at the same lamp.
Perf 4 adds the dynamic-light-shadow removal patch. Perf 7 also removes SSAO,
depth of field, and bloom. Each run used a fresh copy of the starting save.

| Effects setting | Average FPS | 1% low | Worst frame |
| --- | ---: | ---: | ---: |
| Perf 3, control above | 54.77 | 27.72 | 42.35 ms |
| Perf 4 | 49.36 | 21.81 | 108.32 ms |
| Perf 7 | 26.00 | 4.03 | 515.62 ms |

Other work was running on my Mac, including checks for another project during
the perf-7 run. These results do not show the cost of each effect on its own.
They do show that fewer effects did not produce a clean 90 FPS result here.
I checked the scene at both ends, but not combat, sound, or game speed.
My normal profile stays at perf 3.

## Depth states: another promising first lap

I added a small, private cache for Metal depth and stencil states. These
states help decide which pixels to draw. The cache can keep up to 128 states
and reuse a match. It is off by default.

The Intel driver builds. The cache passed 36 checks and 20,000 threaded
lookups with memory-error checks. Those tests cover its keys and object
lifetime. They do not prove that every game renders correctly.

I repeated the same 60-second lamp view with the cache off and on. All four
runs used the same driver, game patch, starting settings, and executable.
I kept 1080p, cap 120, perf 3, vblank 120, and the 64 KiB buffer experiment.
Other timing probes, table reuse, and thread-priority changes were off.

| Cache | Average FPS | 1% low | Worst frame |
| --- | ---: | ---: | ---: |
| Off, first | 29.55 | 14.49 | 125.03 ms |
| On, first | 55.54 | 27.11 | 74.89 ms |
| Off, repeat | 50.15 | 28.91 | 49.96 ms |
| On, repeat | 42.16 | 16.78 | 62.72 ms |

The first gain did not survive the repeat. The second enabled run had 82
frames longer than 50 ms. I have not shown a speedup, so this cache stays
private and off. I checked the lamp view at both ends. Background load and
window focus were not held steady. A later keyboard check did not show
movement, so controls and combat remain unverified for this build.

The driver did not print its shutdown cache counts. I added an optional
probe that reports during play, then made two separate diagnostic runs.
The updated code passed 49 checks and 20,000 threaded lookups.

- Cache off: 475,613 state creations took 857.51 ms across 59.05 seconds.
  That is about 1.45% of the wall-clock time in this scene.
- Cache on: all 338,954 lookups found a match. No new state was made during
  those 59.53 seconds. Lookups took 73.03 ms, or about 0.12% of the time.

The cache does reuse states. But the cost it removes was small in this test.
These are summed CPU call times, not GPU times or proof of an FPS gain.
Probe overhead was not measured. The diagnostic runs averaged 30.63 and
21.89 FPS; the second had a 5.05-second stall. Other work was still running
on my Mac, and I have not pinned down the cause of that stall.

After clicking inside the game window, I checked walking and camera movement
with the cache off and on. Both worked after the timed captures. Combat,
sound, and game speed still need checks. My original saves and settings
remain unchanged. The 90 FPS hunt is still on.

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
