```text
Document:    Bloodborne Launcher Roadmap
Version:     v1.1.0
Author:      Christopher Celaya
Contact:     https://github.com/while-basic
Date:        2026-10-12
SHA256:      c125d72443ddee0819f3df0198a66bf133057926e1f4b29dfbce582e87ebdc37
Chain:       solana-mainnet
Tx:          41WbevVde7GHfLoj6MWVxoXv6oAvs3KKvPxYhZWcHwwxUDq8bbETQxDHYL4nRXPpDKAfkbf5nyDyagCF4oCcSwsc
License:     The Unlicense (public domain dedication)
```

# Roadmap

The order is Mac performance, Windows and Linux, then the web browser.
There are no release dates or guaranteed FPS results yet.

## 1. Mac: work toward 90+ FPS

Current baseline: the owner reports **24–55 FPS** on an M5 Max MacBook Pro with
128 GB unified memory. The goal is **90+ actual gameplay FPS**, not simply setting
a higher FPS cap. Target resolution and quality settings remain to be confirmed.

First record a repeatable baseline: emulator version and binary hash, patch XML
hash, game region/update, macOS build, resolution, cap, performance level, extra
patches, power mode, and display refresh rate. Use the same save location and
route for each comparison. Record cold-cache and warm-cache runs separately.

Report average FPS, frame-time percentiles or 1% lows, stutter, crashes, and
visual differences over several runs. Preserve logs locally and share only
reviewed, non-sensitive results. Do not treat short overlay peaks as sustained FPS.

Then profile emulation/CPU cost, graphics translation, shader compilation, and
frame pacing. Compare upstream emulator updates and settings one change at a
time. Check controls, audio, game timing, and save/load behavior after each change.

**Release gate:** repeatable 90+ FPS gameplay at a stated resolution and quality,
with the test duration, scene, lows, and limitations published. Performance
depends on upstream emulation and graphics work; this wrapper alone may not
achieve the target.

## 2. Windows and Linux optimization

After the Mac performance work, add platform-aware paths, engine selection,
process checks, and launch instructions. Test native Vulkan drivers and measure
the same gameplay route on named Windows and Linux hardware.

Document OS version, CPU, GPU, RAM, driver, emulator revision, and results for
each machine. Validate clean setup, controller input, audio, fullscreen, config
backup/restore, and save/load behavior. Keep each platform's support status separate.

**Release gate:** another owner can follow a clean setup and reproduce a stable
play session on each documented platform. Upstream support alone does not
qualify this launcher.

## 3. Web browser research

Browser support comes last. Decide whether the goal is local browser execution
or streaming from a user-owned computer before choosing the design.

Local execution would require substantial emulator/runtime work, including
CPU translation, graphics through browser APIs, storage, threading, memory
limits, and controller/audio support. A native macOS launcher cannot simply be
packaged as a browser build. Streaming is a different product with a host
emulator and network/input latency.

**Release gate:** a documented proof of concept, a clear architecture choice,
measured input latency and performance, and an explicit list of supported
browsers/devices. No native browser playability or 90+ FPS claim is made today.

## Update notes

| Date | Change |
| --- | --- |
| 2026-10-12 | Prepared public setup docs, recorded the M5 Max / 128 GB test machine and owner-reported 24–55 FPS, and set the phase order above. |

Future entries should state what changed, which build was tested, measured
results, and any new limits. Run checks locally; do not use GitHub Actions.
