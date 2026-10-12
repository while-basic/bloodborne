```text
Document:    Bloodborne Mac Performance Investigation
Version:     v1.2.0
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-10-12
SHA256:      842c52c1ea967f7179a5908790a611887a132e27f6e75e231d8bc075fa449c3b
Chain:       solana-mainnet
Tx:          YY7nudrXgGivSR7K19naFE23jXUHCcUiShXsWVHRpHvdMeNkdePvSKJbesXu5BYVtuc2XQANQv5uNdQxnyEN1Py
License:     All Rights Reserved / Celaya Solutions
```

# Current working profile — October 12, 2026

The restored **1080p / 60 FPS target / performance level 3** run was reported as
“very good.” Keep this as the starting point for the next session. This is a
report about how the game felt; no FPS number or frame-time measurement was
collected for that run.

```sh
python3 play.py --resolution 1080p --fps 60 --perf 3 --engine nightly \
  --fullscreen-mode borderless --present-mode Mailbox --vblank 60
```

The nightly binary, performance patches, and fullscreen mode stayed the same
across the comparison. The driver does not support Mailbox and logs a fallback
to Fifo. The FPS overlay is set to `fps_scale=2.500000` in shadPS4's `imgui.ini`;
that is a local display setting, not an FPS improvement.

| Attempt | Result | Evidence |
| --- | --- | --- |
| 1080p before the resolution change | Reported as somewhat smooth | 212 seconds of continuous activity recording |
| 900p, same 60 FPS target and performance level 3 | Reported as extremely laggy at the boss | 234 seconds of continuous activity recording; runtime 1600×900 buffers verified |
| Restored 1080p | Reported as very good | Runtime 1920×1080 buffers verified; config matched the pre-test backup |

The 900p resolution patch was removed after that test. No saves were rolled
back. The earlier three-minute capture expired before the death report was
processed, so it cannot establish whole-fight coverage. The two later captures
continued until the user reported death. Their exact combat and death times
were not observed, and they include travel/loading. Do not use whole-run
averages as a boss-only benchmark.

For the next session:

- Start from the working 1080p profile above; do not reapply 900p by default.
- Use only the lightweight recorder while playing. It reads CPU/GPU activity,
  not the screen or FPS. Wait for the user to report death before stopping it.
- Use `--seconds 3600 --interval 2` for travel and a boss attempt; renew the
  recorder if its one-hour limit approaches. Stop only the recorder with
  Ctrl-C or SIGINT. An intentional interruption preserves the samples and
  writes a summary with `complete: false` and `KeyboardInterrupt`.
- Mark menu, travel, combat, and death reports in the local event log. Do not
  infer a death or FPS drop from utilization alone.
- If more diagnosis is needed, first collect readable FPS or frame times from
  the same scene. Heavy Metal/Instruments tracing must stay off during play.

Private evidence stays under `runtime/`: the 1080p and 900p attempts are
`profiles/20261012T172604681876Z/` and `profiles/20261012T173400966672Z/`.
The restored session log is
`sessions/20261012-113851-196746-1080p-60-perf3-nightly.log`.
The pre-test settings and save backup is
`test-backups/20261012T173220Z-before-900p/`. Keep these files out of Git.

# Native-port findings

The provided Codex folder contains the owner's PS4 backup, game packages, packaging
tools, and emulator downloads. Its `eboot.bin` is an x86-64 FreeBSD ELF executable,
not game source that can be compiled for Apple silicon.

The running emulator is shadPS4 0.19.1 WIP, revision
`e0a466753a1aacbc8db8253be685bf7ab4d9daae`. The installed executable is x86-64 and
runs under Rosetta. Its session log selects the Apple M5 Max through KosmicKrisp
26.2.99; the process loads the Metal driver. GPU rendering is already active.

The matching upstream source accepts ARM64 as a build architecture, but
[`RunMainEntry`](https://github.com/shadps4-emu/shadPS4/blob/e0a466753a1aacbc8db8253be685bf7ab4d9daae/src/core/linker.cpp#L41-L64)
ends with `RunMainEntry unimplemented for current architecture` outside x86-64.
An ARM build alone therefore cannot start this game. A native port requires game
source or a substantial binary translation/recompilation and PS4 compatibility
project. A native Metal renderer would address graphics translation only.

# Measurements and their limits

Initial one-second observation before the reported death: Game:Main used 81.2%
of one CPU core, the GPU command processor 65.6%, and Rosetta's exception server
42.6%. A separate instantaneous whole-machine GPU reading was 75%; it was not a
synchronized game-only measurement.

The user then reported dying. The following captures span the post-death period;
the visible game scene was not confirmed and no FPS was measured. These are
diagnostic captures, **not a crowded-scene benchmark or proof of a speedup**.

| Capture | Duration | Main thread median | GPU command thread median | Rosetta exception thread median |
| --- | ---: | ---: | ---: | ---: |
| travel-1 | 60 s | 74.02% | 11.98% | 27.98% |
| travel-2 | 180 s | 73.53% | 12.06% | 28.35% |

100% means one CPU core. Whole-machine GPU use had medians of 16.5% and 0% in
these runs, respectively. It includes other apps and cannot establish the game's
GPU frame time. A busy CPU thread alone also does not prove what limits FPS.

A 15-second Instruments Time Profiler recording captured 18,347 raw sample rows.
Timer samples concentrate on Game:Main and Rosetta's exception server. The main
thread mostly ran on the M5 Max's super cores, so it was not simply stuck on a
slower core. Game addresses lack source symbols; no exact hot game function has
been identified.

macOS `sample` crashed while unwinding this process. Instruments recording and
raw `time-sample` export succeeded; derived `time-profile` backtrace export
crashed in Apple's exporter. The raw recording and exports remain local under
`runtime/profiling-20261012/`. Raw Instruments traces can contain process
environment values and must remain private and untracked.

# Confirmed play session at 11:02–11:08 local time

The user said play was starting and then reported extreme lag during a boss
fight. The old process exited as the first capture began; that four-sample run
is incomplete and excluded. A new emulator process, PID 60641, was detected and
recorded for 120 seconds (59 samples). Settings remained 1080p, 60 FPS cap, perf
level 3, with Disable Facegen enabled.

Before the heavier trace began, a 39-second normal-play window showed medians of
79.3% for Game:Main, 74.0% for the GPU command processor, 50.8% for Rosetta's
exception server, and 78.5% whole-machine GPU utilization. This was a changing
play scene, not a fixed-camera A/B test.

A 20-second Metal System Trace was attempted. Its recorder spent several more
minutes processing, reached about 176% CPU and 16 GB resident memory, and produced
a large partial trace. This overlapped the user's report of boss-fight lag and
may have contributed to it. SIGINT did not promptly stop processing, so SIGTERM
was sent to the profiler only. The profiler was verified absent and the game
remained running. **The trace is incomplete, and its overlap period is excluded
from normal-performance conclusions. Do not repeat heavy tracing during combat.**

A fresh, light 60-second capture after the heavy profiler was stopped produced
30 complete samples:

| Measurement | Median | Range |
| --- | ---: | ---: |
| Game main thread, one-core CPU percentage | 82.19% | 79.89–83.58% |
| GPU command processor, one-core CPU percentage | 69.61% | 67.97–76.43% |
| Rosetta exception server, one-core CPU percentage | 48.69% | 46.66–51.45% |
| Whole-machine GPU utilization | 74% | 70–91% |

The GPU is active, and there is sustained CPU work in game execution, graphics
command processing, and Rosetta exception handling. These counters do not prove
which stage limits frame rate. The user has not supplied an FPS number, and a
valid GPU frame-time trace was not obtained. At that point, whether the perceived
boss-fight lag eased after stopping the trace had not been confirmed. The later
resolution comparison and restored 1080p result are recorded above.

Evidence is private under `runtime/profiles/20261012T170225632651Z/` (mixed
startup/play/trace run, context, and event log) and
`runtime/profiles/20261012T170731024562Z/` (clean light follow-up). No emulator
settings, game files, or saves were changed.

# Repeatable passive capture

Run this while the existing game is active:

```sh
python3 profile_runtime.py --seconds 3600 --interval 2 --label "travel and boss attempt"
```

The recorder reads macOS thread counters and Apple GPU counters every two
seconds. It never sends input, changes emulator settings, restarts the game, or
edits saves. It writes metadata, timestamped samples, and a thread summary into
a new directory under `runtime/profiles/`. GPU values are explicitly labeled
whole-machine values; scene and FPS are not inferred. Use `--pid` if multiple
emulators are running. Existing output directories are rejected to preserve
earlier evidence. Interrupted captures retain their data and report incomplete.

Validation: a separate busy Python thread measured 98.16% of one core over six
samples; all samples included GPU counters. Invalid PIDs fail clearly, and an
attempt to reuse an output directory left the original summary unchanged.

# Next optimization gate

First obtain two stable captures at the same busy outdoor location, with the
same camera, resolution, patches, and warm shader cache. Record the visible FPS
alongside the capture and exclude death/loading intervals. Use a low-overhead frame-time source to distinguish graphics work from waits;
the heavy Metal trace attempted above disturbed the run and is not suitable
while the user is fighting.

The observed Rosetta exception load makes CPU compatibility and memory tracking
worth inspecting, but does not establish the cause. The matching source handles
memory tracking through signals on macOS (`src/video_core/page_manager.cpp`,
`SignalImpl`); the alternative userfaultfd implementation is Linux-only. The next
emulator experiment should count and time those faults and CPU compatibility
handlers in a local instrumented build before changing their behavior. Do not
disable memory protection or assume direct-memory-access settings are a fix.

The 900p trial changed resolution and was reverted after worse reported play.
No native port or renderer replacement has been delivered. The restored 1080p
result above is reported play quality, not a measured FPS increase.
