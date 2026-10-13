```text
Document:    My Bloodborne Frame Capture Guide
Version:     v1.1.0
Author:      Christopher Celaya
Contact:     https://github.com/while-basic
Date:        2026-10-13
SHA256:      d1d4a41f8562b87e0f3f046979b2252264ff7c8fd45b5d58303a5fbe9cf73a86
Chain:       solana-mainnet
Tx:          27GTo6pzzF3Dbo1HvEJnXvmRXvnqB2PgpzW3U8xUE6aY4GkKDeWcWx4Ls9b6BzBqQSqh6bL5hNpkhN3Rp1fWDFr5
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

## License

The emulator patches change shadPS4 and follow its **GPL-2.0-or-later** terms.
It is not covered by this repo's Unlicense dedication. My analyzer and this
guide are original work under the Unlicense. Keep shadPS4's credits and license
when sharing any modified emulator build.
