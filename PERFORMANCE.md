```text
Document:    Bloodborne Mac Performance Investigation
Version:     v1.0.0
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-10-12
SHA256:      d75dba805d8d52ac8b98b647bdd8d909072122d08a5b7e90af3d97e08c904914
Chain:       solana-mainnet
Tx:          5FAo9LBALJ9C1iPszyAwrfxbamissFEQZ49aPcmLBovsvisLH2XJq2QeCMkbLho8ciDNUTBWoh635TogWaZV1Nt1
License:     All Rights Reserved / Celaya Solutions
```

# Findings

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

# Repeatable passive capture

Run this while the existing game is active:

```sh
python3 profile_runtime.py --seconds 60 --label "standing in Central Yharnam"
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
alongside the capture and exclude death/loading intervals. Then collect GPU
frame timing with Metal System Trace to distinguish graphics work from waits.

The observed Rosetta exception load makes CPU compatibility and memory tracking
worth inspecting, but does not establish the cause. The matching source handles
memory tracking through signals on macOS (`src/video_core/page_manager.cpp`,
`SignalImpl`); the alternative userfaultfd implementation is Linux-only. The next
emulator experiment should count and time those faults and CPU compatibility
handlers in a local instrumented build before changing their behavior. Do not
disable memory protection or assume direct-memory-access settings are a fix.

No emulator or game performance settings were changed during this investigation.
No native port, renderer replacement, or FPS improvement has been delivered.
