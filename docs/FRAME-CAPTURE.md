```text
Document:    My Bloodborne Frame Capture Guide
Version:     v1.0.0
Author:      Christopher Celaya
Contact:     https://github.com/while-basic
Date:        2026-10-13
SHA256:      73d662fb2d3528e92425ea92d674f4c2d025139c8f06f672e7ab3681b1e96ac2
Chain:       solana-mainnet
Tx:          49miAzJDXvzpuh89cVeyvoTGXWZ9Fo9YZQvfHmo4mDCDkfQGWVr6Ep1Ccyi5NxLJy1CJ6wgnKR1gqin1bXhkcSSs
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

## License

The emulator patch changes shadPS4 and follows its **GPL-2.0-or-later** terms.
It is not covered by this repo's Unlicense dedication. My analyzer and this
guide are original work under the Unlicense. Keep shadPS4's credits and license
when sharing any modified emulator build.
