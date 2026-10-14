```text
Document:    My Bloodborne Mac Performance Notes
Version:     v2.13.0
Author:      Christopher Celaya
Contact:     https://github.com/while-basic
Date:        2026-10-13
SHA256:      8c5ae976eb121ec7dee7b5ae14ef6d771d7a9469f155f8b2b2b4d9eb2f252657
Chain:       solana-mainnet
Tx:          4LFZutmvYj9CMdBfMpM5pMXukUtF8cNg2GKjxqPYbYV84nHofXv34PsNiJ85iENLU9aYfCaNCfvbKVv9UHiAeQ2V
License:     The Unlicense (public domain dedication)
```

# Hunting the missing frames

## Stopping point — October 13, 2026

I prepared a GPU feedback probe using shadPS4's existing Metal start/end timing
hooks. LaunchServices confused the copied app with an older probe, so I did not
get a valid GPU capture. I made no GPU change and do not claim a speedup. The
next useful lead is to repeat the probe with a unique bundle identity, then
compare the same busy scene against the working 1080p profile.

I then reran the probe with a fresh local save copy and an explicit
`KK_GPU_TIMING_LOG` path. It wrote 13,459 GPU feedback rows with no reported
errors. In the short post-load slice, GPU command residence averaged 0.31 ms,
with a 1.07 ms 95th percentile and a 1.63 ms maximum. This automated route is
diagnostic evidence only: it does not show a busy fight, prove a frame-rate
floor, or justify a GPU optimization. The next code lead is CPU and Rosetta
work around the frame path, while the working 1080p profile stays unchanged.

I also tried `Immediate` present mode in a matching automated route. It averaged
about 103 FPS, compared with about 101 FPS in the prior route. That small change
is not a gameplay result and may trade away tear-free presentation, so I left
the public default alone.

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

## Following the draw calls

I added an optional timer to my private driver build. It samples one draw in
64 and changes the sample slot each time. It reads no clocks when switched
off. The test checks passed, including eight separate recording threads.

In one lamp-view capture, the main draw thread recorded 25,468 samples from
about 1.63 million draws. Pipeline setup took **29.81%** of the sampled draw
time. Changing draw state took **19.08%**, and sending the draw took
**19.12%**. Those shares describe time inside the sampled calls. They are
not shares of a whole frame or GPU time. The clocks and time spent waiting
for a CPU turn are included.

That diagnostic run averaged **26.36 FPS**, with a **10.00 FPS 1% low** and
a worst frame of **125.06 ms**. Other apps were running. I have not measured
the timer's overhead, so I am using this run to choose what to study next.

## Reusing the same shader setup

My next private driver change skips a shader bind when the same shader is
already set and has no pending reset. A new drawing pass still gets its
full setup. The build passed, along with 10,000 comparisons against the
old method and checks for resets and memory errors.

One early test moved away from the starting view. I threw out its speed
comparison. I then added an optional F9 input lock to my test build. It
blocks game input until that test app closes. Menu input worked before
the lock; walking and camera keys had no effect after it. The lock also
passed 65 code checks. It stays out of normal play.

Here are four new runs in order. Each used a fresh copy of my saves, the
same app and driver, 1080p, a 120 FPS cap, perf 3, and the 64 KiB buffer
experiment. I locked input and checked the lamp view at both ends. Each
capture lasted 60 seconds after a 30-second warmup. The extra timing
probes were off.

| Shader reuse | Average FPS | 1% low FPS | Worst frame | Frames over 50 ms |
| --- | ---: | ---: | ---: | ---: |
| Off | 46.11 | 17.05 | 150.05 ms | 13 |
| On | 50.63 | 18.52 | 191.78 ms | 8 |
| Off again | 42.42 | 16.19 | 191.71 ms | 9 |
| On again | 50.44 | 22.79 | 66.75 ms | 9 |

Both enabled averages beat both controls. That is a useful lead, but other
apps were still working and I did not track focus for the whole capture.
The first enabled run also had a worse longest frame. I am keeping this
change private and off by default while I check it further. A still view
does not test combat, sound, controls, or game speed. **90+ FPS is still open.**

All 16 original save files still match their backups. My original settings
now differ only in volume, which changed from 100 to 0. I left that change
alone. The tests used separate settings and copied saves.

## Vertex setup: fewer calls did not pay off

I tried reusing vertex buffer bindings when their address and size stayed the
same. The code still updates strides and keeps pending state changes. It passed
40,000 comparisons with the old method, plus sanitizer and thread checks.

A separate live counter test saw 3,379,200 calls over 58.89 seconds. Only 5.23%
of bindings stayed the same. About 7.03% of calls avoided marking vertex data as
changed. That does not prove the later GPU data upload was skipped.

With those counters off, I ran the same locked lamp view for a minute each:

| Vertex reuse | Average FPS | 1% low FPS | Worst frame | Frames over 50 ms |
| --- | ---: | ---: | ---: | ---: |
| Off | 56.28 | 28.94 | 41.74 ms | 0 |
| On | 45.89 | 4.06 | 816.71 ms | 79 |

The build, starting settings, game patches, and view matched. Shader reuse was
on in both runs. Other work on the Mac was still outside my control, so I cannot
blame every stall on this change. I have no speed win to keep here. This private
experiment stays off.

## Fewer effects, one setting at a time

I tried the lighter picture again with the same signed build, 1080p, a 120 FPS
cap, vblank 120, and the 64 KiB buffer experiment. Shader reuse stayed on. Vertex
reuse and all extra probes stayed off. Mailbox still fell back to Fifo.

This time I changed only the effect level between these four runs. Perf 7 adds
four cuts to perf 3: dynamic light shadows, SSAO, depth of field, and bloom. That
means fewer shadows, less shading in corners, less lens blur, and less glow.
The picture changes. These are not free frames.

| Effect level | Average FPS | 1% low FPS | Worst frame | Frames over 50 ms |
| --- | ---: | ---: | ---: | ---: |
| Perf 3 | 56.28 | 28.94 | 41.74 ms | 0 |
| Perf 7 | 71.11 | 38.61 | 41.64 ms | 0 |
| Perf 3 again | 56.38 | 33.62 | 51.31 ms | 2 |
| Perf 7 again | 71.34 | 36.59 | 58.26 ms | 1 |

Each test used fresh copied saves, locked controls, 30 seconds of warmup, and
60 seconds of frame logging. I checked the lamp and camera view at both ends.
Both lighter-effects runs beat both normal-effects runs in this view. Other
apps and focus were not tracked through the whole test, and I have not repeated
combat or sound checks. This is useful progress, not a 90 FPS gameplay result.
My usual 1080p / 60 cap / perf 3 profile stays intact.

I then tried perf 7 at 720p with the same build and flags. That one-minute run
averaged **73.75 FPS**, with a **39.39 FPS 1% low**, a **33.41 ms worst frame**,
and no frames over 50 ms. The view matched at both ends. It was one run, and the
small difference does not make 720p a proven win. Cutting the pixel count did
not get this scene to 90 FPS.

## A CPU fallback path I ruled out for this scene

Some short SSE4a instructions can fall back to an interpreter each time they
run. I added counters to see if that was happening here. The counters passed
sanitizer checks, 800,000 events from eight threads, and 1,000 live signal calls.
The signal path uses lock-free counters. A separate thread writes once a second.

In the locked lamp scene, 57 snapshots covered 59.09 seconds. The short EXTRQ,
short INSERTQ, illegal-instruction patch, and access-fault patch counters all
stayed at **zero**. These counters cover the patcher, not every memory fault in
the emulator. I have no evidence that this fallback path is a useful speed
target for this view. The diagnostic stays off during normal tests.

## Counting memory faults

I added a separate counter for memory tracking. A write fault means the game
touched a page that the emulator was watching for changes. Handling many of
these calls may cost time, so I counted them before changing more code.

| Buffer write group | Counter window | Write faults per second |
| --- | ---: | ---: |
| 64 KiB experiment | 58.96 s | 3,139 |
| Original narrow range | 59.50 s | 27,372 |

Both used the same diagnostic build and the locked lamp view. Neither counted
read faults or unhandled faults in these windows. The wider setting removed
many fault-handler visits, but both frame captures had long stalls. I do not
use their FPS values to claim a gain. Other apps and probe overhead were not
controlled. Counts are not time spent handling each fault.

The older frame log flushes every 120 samples. Its last row can be old, so the
first counter-to-frame ratios were only rough estimates. I added a small
[clock patch](docs/FRAME-CAPTURE.md#match-frames-to-other-counters) to line up
future records. It runs the extra clock check once. The Release build and
sanitizer checks pass, including checks that old output files stay untouched.

With that clock reference, a fresh 64 KiB run counted about **122 write faults
per presented frame**. The matching original-range run counted about **900**.
Their counter windows lasted 59.15 and 59.40 seconds. Both clock checks took
less than five microseconds. These are still approximate ratios: the counters
are read one by one, and neither run controlled other apps. I have not accepted
an FPS gain from this pair. I then measured the normal buffer work that follows
these faults, keeping the new timing calls out of the signal handler.

## Time spent on buffer work

I added an optional timer to the private test build. It measures time inside
buffer calls. It stays off by default. The Release build and sanitizer checks
pass, including checks for several threads, nested calls, and old log files.

I tested the 64 KiB group and the original range with the same signed app,
settings, patches, copied save, and locked lamp view. Each capture lasted about
60 seconds. The timer covered 59.00 and 59.04 seconds of full log windows.

| Time inside a call, as part of the 60-second test | 64 KiB | Original range |
| --- | ---: | ---: |
| Fetch a buffer, including work inside it | 18.64% | 16.45% |
| Upload a small stream buffer | 5.68% | 4.59% |
| Track changed ranges | 2.73% | 2.59% |
| Copy changed data to staging memory | 1.28% | 0.71% |
| Queue buffer upload commands | 1.70% | 1.91% |

These times overlap. **Do not add the rows.** They include time spent waiting
and the timer's own cost. They do not measure CPU use or time on the GPU.
The wider setting also copied more data per staging request, so fewer faults
come with a tradeoff.

The diagnostic frame logs averaged 35.16 and 26.36 FPS. Other apps were not
controlled, and I did not measure the timer's overhead. I do not count this
pair as an accepted speed gain or compare it with the earlier 71 FPS runs.
It does not show that buffer work alone can close the gap to 90 FPS.

I stopped here with both test apps closed. All 16 original save files and my
current settings still match. Next time, I can use the driver's existing GPU
start/end feedback to separate GPU work from time on the host. I inspected
that path but have not changed it or taken a GPU timing capture.

## A fresh clock check

I tried vblank 240 again with the lighter perf-7 picture and shader reuse on.
That run averaged **37.65 FPS**. A fresh vblank-120 control averaged **39.57 FPS**.
Each used the same signed build, game patches, copied save, and locked lamp
view for about 60 seconds. Other apps were busy, so I do not compare this pair
with the earlier 71 FPS runs. This pair does not support a faster clock setting.

I also tested repeated Metal depth-state calls in a small, separate program.
The usual call took about 13 nanoseconds in that test. It made no draws and
submitted no GPU work, so it is not a game benchmark. I left that driver code
alone and moved on to memory tracking.

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
