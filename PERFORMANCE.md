```text
Document:    My Bloodborne Mac Performance Notes
Version:     v2.1.0
Author:      Christopher Celaya
Contact:     https://github.com/while-basic
Date:        2026-10-13
SHA256:      7edefa0034f6b353bd690ae8c1da9b2febf909f3987e17b403355567d7d5ad6c
Chain:       solana-mainnet
Tx:          3Z9kNs4bwsDEJ7wziRhnnQVuFpq2vE5nQxZeUitBwTJRqQLuu1jtVA7n6xqrJr8koacyQYgkGrToZsyHQMx7S8J7
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
