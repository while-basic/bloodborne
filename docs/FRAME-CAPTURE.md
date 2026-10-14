```text
Document:    My Bloodborne Frame Capture Guide
Version:     v1.4.0
Author:      Christopher Celaya
Contact:     https://github.com/while-basic
Date:        2026-10-13
SHA256:      e33c4ccd68358d20275ab2ea835fefd37eeb81825d5afdbbe6c2154a14d43baf
Chain:       solana-mainnet
Tx:          2LKSPkW4ShzyLihUHTL9BuStdPQxwbuhXTQy3pUJjoryvpEtGMVjYsDLaLuRYVwwJLnd8Lq2X5pnusVTkk2X1G6B
License:     The Unlicense (public domain dedication)
```

# Count frames, not wishes

I added an optional frame logger for a local shadPS4 build and a small Python
tool to read it. This is test gear for the 90+ FPS work. It does not speed up
the game, and it does not replace the regular launcher.

The [patch](../patches/shadps4/frame-timing.patch) targets shadPS4 commit
[`e0a4667`](https://github.com/shadps4-emu/shadPS4/commit/e0a466753a1aacbc8db8253be685bf7ab4d9daae).
It records the intervals used for the emulator's FPS counter. Reused frames
are skipped. These are presentation intervals, not GPU execution times.
It cannot tell a menu from a boss fight.

## Build and record

Ask permission before a load test. Keep the normal emulator, config, patch
profile, and saves backed up. Use a separate source worktree and a separate
copy of shadPS4's state. Follow the
[upstream Mac build guide](https://github.com/shadps4-emu/shadPS4/blob/e0a466753a1aacbc8db8253be685bf7ab4d9daae/documents/building-macos.md).
I built this patch locally with the Release configuration for x86-64.

1. Check out the source commit above and initialize its submodules.
2. Apply the patch from this repo, using its real absolute path:

   ```sh
   git apply --check /path/to/bloodborne/patches/shadps4/frame-timing.patch
   git apply /path/to/bloodborne/patches/shadps4/frame-timing.patch
   ```

3. Build with the upstream instructions. If you reuse an installed Mac driver
   with `ENABLE_SYSTEM_VULKAN=ON`, keep its `libvulkan.dylib`,
   `libvulkan_kosmickrisp.dylib`, and JSON driver file beside the new executable.
   That engine revision looks there for the driver. Record the driver hash.
4. Create a private test folder containing a **copied** `user/` directory.
   This is shadPS4's portable state layout. Include the needed settings,
   modules, input config, and copied saves. Run from that test folder and check
   the log confirms its private paths. Do not link your only save into it.
5. Set a fresh output file before launching the patched executable:

   ```sh
   SHADPS4_FRAME_LOG="$PWD/frames.csv" /path/to/patched/shadps4 \
     --show-fps --game /path/to/my/game/eboot.bin
   ```

The file is created only when the environment variable is set. An existing
file is refused, so choose a new name for each run. Output is buffered and
flushed every 120 samples. A crash or forced stop can lose the unflushed tail.
End the game normally when possible and label interrupted runs.

## Match frames to other counters

The CSV is buffered. Its last visible row can be a few seconds old. I do not
use that row as the current time when lining up frames with another recorder.

For new captures, apply my [clock patch](../patches/shadps4/frame-clock-origin.patch)
after the frame-timing patch and before building:

```sh
git apply --check /path/to/bloodborne/patches/shadps4/frame-clock-origin.patch
git apply /path/to/bloodborne/patches/shadps4/frame-clock-origin.patch
```

It creates `frames.csv.origin.json` beside a log named `frames.csv`. This
small file records the time at elapsed zero. Add a CSV row's `elapsed_seconds`
to `unix_seconds_at_elapsed_zero` to line it up with wall-clock records.
`calibration_span_seconds` tells me how long the clock check took.

The extra clock check runs once. It adds no clock calls to later frames.
Existing files are left alone. Recording stops if either output already exists.
Use a fresh folder, check that both files were created, and keep the same patched
build for both sides of a comparison.
Clock changes or large calibration gaps can still spoil the match. The CSV
format and the analyzer commands below stay the same.

## Read a known scene

Write down when the observed scene begins and ends, using the CSV's elapsed
seconds. Then run this from the Bloodborne launcher repo:

```sh
python3 analyze_frames.py runtime/my-test/frames.csv \
  --start 60 --end 120 --label "1080p, same outdoor route, warm cache, run 1"
```

The numbers above are examples, not recorded results. Only include the part
you actually observed. The tool excludes frames crossing the chosen start
or end. Use `--label "unobserved"` when you cannot identify the scene; that
result cannot verify gameplay performance.

I report average FPS from total frame time, the median and slow frame times,
the worst frame, and a 1% low. Here, the 1% low is 1,000 divided by the mean
duration of the slowest 1% of frames. It is not the same as a percentile of
sampled on-screen FPS.

Bad numbers, backward timestamps, missing rows, and an empty selected interval
fail with an error. The result always says the tool did not verify the scene.
The share of frames within the 90 FPS budget is only a timing statistic.
It does not certify steady 90+ gameplay, correct game speed, or picture quality.

Use the same instrumented build for both sides of a comparison. First measure
the logger's overhead against an unmodified build. Keep power mode, display,
scene, camera, cache, driver, and patches fixed. Repeat runs and keep raw data
under ignored `runtime/` folders. Do not upload saves or logs.

## Optional buffer-reuse fix

I found a small bug in the same pinned emulator source. Its buffer pool checks
an old copy of the GPU's progress even after asking for a fresh value. That can
make it create extra command buffers when a ready one could be reused.

The [reuse patch](../patches/shadps4/resource-pool-refresh.patch) fixes that
check. It is separate from the frame logger. It is not a 90 FPS patch.

From the shadPS4 source checkout, before building:

```sh
git apply --check /path/to/bloodborne/patches/shadps4/resource-pool-refresh.patch
git apply /path/to/bloodborne/patches/shadps4/resource-pool-refresh.patch
```

From this launcher repo, run the small code check with a C++20 compiler:

```sh
python3 check_resource_pool.py /path/to/shadPS4
```

This compiles the actual pool class and methods from that trusted checkout.
A small test clock stands in for GPU progress. The old source fails two reuse
cases; the patched source passes all five checks. It also checks that a busy
pool still grows. It does not launch a game or prove an FPS gain. Temporary
test programs are removed when the check ends.

Build and compare the game separately, using the same scene and settings.

## Optional buffer-write experiment

I am testing a separate
[memory-tracking patch](../patches/shadps4/buffer-write-window.patch) on my M5 Max.
On a write fault, it can mark a 16, 64, or 256 KiB group of buffer memory as
changed. It only widens the check when the whole group is mapped and contains
the original request. Texture checks keep their original range. The feature
is **off by default**.

Use the same pinned source and a separate copy of your settings and saves.
Ask permission before the load test. Apply the patch before building:

```sh
git apply --check /path/to/bloodborne/patches/shadps4/buffer-write-window.patch
git apply /path/to/bloodborne/patches/shadps4/buffer-write-window.patch
```

From this launcher repo, check the changed methods:

```sh
python3 check_buffer_faults.py /path/to/shadPS4
```

This needs a C++20 compiler and shadPS4's Boost submodule. It checks 40 memory
cases and 14 setting combinations against the changed source. These include
gaps, address overflow, requests that cross a group, and the unchanged texture
range. The checks do not test thread safety, combat, or FPS.

After building, run the same copied save twice. Keep every setting fixed and
choose a new frame log each time. Run these from your private test folder:

```sh
# Control: ordinary buffer tracking.
SHADPS4_BUFFER_WRITE_WINDOW_KIB=0 SHADPS4_FRAME_LOG="$PWD/control.csv" \
  /path/to/patched/shadps4 --show-fps --game /path/to/my/game/eboot.bin

# Experiment: try a 64 KiB group for buffer writes.
SHADPS4_BUFFER_WRITE_WINDOW_KIB=64 SHADPS4_FRAME_LOG="$PWD/experiment.csv" \
  /path/to/patched/shadps4 --show-fps --game /path/to/my/game/eboot.bin
```

Use `0`, `16`, `64`, or `256` for the group size. Bigger was not always faster
in my tests. Repeat the control after each trial, and compare slow frames too.

The old `SHADPS4_WRITE_FAULT_WINDOW_16K=1` switch still selects 16 KiB. A valid
new setting takes priority over it, including `0` to turn the feature off.
Other values are ignored. Leave both switches unset for ordinary tracking.
My results and their limits are in [the performance notes](../PERFORMANCE.md).
This experiment does not change the normal launcher profile or meet the
90+ FPS goal.

## License

The emulator patches change shadPS4 and follow its **GPL-2.0-or-later** terms.
They are not covered by this repo's Unlicense dedication. My analyzer and this
guide are original work under the Unlicense. Keep shadPS4's credits and license
when sharing any modified emulator build.
