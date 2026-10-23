```text
Document:    My DS3 to Bloodborne Metal Comparison
Version:     v1.0.0
Author:      Christopher Celaya
Contact:     https://github.com/while-basic
Date:        2026-10-22
SHA256:      40505ec5e3aab30b7f7493f647a6b4f4cdf77fc2b55baaa54394e456820d4d95
Chain:       solana-mainnet
Tx:          3gLqXyJk3ko8LLc5WnJJE8q7ynL24aN7D1dKazfTXnmExSbLSfAhTuzLDMNiahJCMxxpSfatdqa7MtoQY8RVkJyy
License:     The Unlicense (public domain dedication)
```

# Bringing my DS3 Metal work to Bloodborne

I reviewed `ds3-mac` at `cc463a0dde225a814415136dda55e583feacb42c`
and Bloodborne at `4f876cc`. Both launch bbport. Neither Python repo contains
a Metal renderer. The graphics path is:

```text
PS4 game code under Rosetta 2
  -> bbport / shadPS4 video core (Vulkan)
  -> Mesa KosmicKrisp (Vulkan on Metal)
  -> Apple Metal

bbport temporal upscaler
  -> exported Metal heaps + scene color, depth, motion vectors
  -> Apple MetalFX temporal scaler
  -> Vulkan presenter
```

## The Apple frameworks and implementation

**Metal.framework** provides the GPU device, command buffers, heaps, textures,
and shared events. **MetalFX.framework** provides `MTLFXTemporalScaler` for
temporal anti-aliasing and upscaling. Native AA keeps render and output sizes
equal; it does not create extra frames.

I checked the shared engine at `97b9e62acd0a53d7b405730b5092b1f9de2f0df9`.
These are engine paths, not files inside this launcher repo:

| Source | What it does |
| --- | --- |
| `gpu/CMakeLists.txt:135` | Builds the Objective-C++ shim with ARC and links Metal and Foundation. MetalFX loads at runtime so a missing framework slice does not stop startup. |
| `gpu/shim/bbport_metalfx.mm:20` | Loads MetalFX with `dlopen`, finds `MTLFXTemporalScalerDescriptor`, checks the device, and creates the scaler. |
| `gpu/shim/bbport_metalfx.mm:195` | Uploads color/depth/motion into Metal textures, sets jitter and motion scale, encodes the scaler, and copies its output back. Shared events coordinate Vulkan and Metal when enabled. |
| `gpu/shadps4/video_core/renderer_vulkan/vk_metalfx.cpp:36` | Checks exportable Metal memory, gets Metal heap handles through `VK_EXT_external_memory_metal`, and connects the scaler to the Vulkan renderer. |
| `gpu/shim/bbport_settings.cpp:137` | Reads `BB_UPSCALER`, `BB_UPSCALE_PRESET`, and `BB_FSR_SHARPNESS` after saved settings. These controls also exist in the pinned `0.4-v1` release. |

The base scaler is already in [bbport 0.4-v1](https://github.com/bmy/bbport-mac/tree/0.4-v1).
I do not need to replace KosmicKrisp or write a second renderer to request it.
The local engine has unrelated changes; I did not build or change it here.

## The first settings I brought over

My references are DS3's `docs/superpowers/specs/2026-10-21-metal-performance-design.md`,
its launcher tuning and engine plans, `docs/runtime.md`, and `play.py:18-49`.
The DS3 project credits CSR (Celaya Solutions) and uses MIT; the engine patches
here keep their existing GPL terms. These are the settings I can reuse:

| DS3 setting | Bloodborne implementation |
| --- | --- |
| MetalFX Native AA | Optional `--metalfx`: `BB_UPSCALER=metalfx`, `BB_UPSCALE_PRESET=0`, `BB_FSR_SHARPNESS=0`. Render/output stay equal at your selected resolution. |
| Larger staging pool and write-fault window | Optional `--tuned`: `BB_STAGING_KEEP_MB=2048`, `BB_FAULT_WINDOW=1024`. These values have DS3 evidence, not a Bloodborne measurement. |
| Unpaced vblank and no Retina scaling | The same `--tuned` sets `BB_VBLANK_HZ=0`, `BB_RETINA=0`. Bloodborne's requested FPS cap remains 60 by default. Add `--windowed` explicitly to match DS3's window mode. |
| Mesa disk shader cache | Every launch sets `MESA_SHADER_CACHE_DIR=runtime/cache/mesa` as an absolute path and `MESA_SHADER_CACHE_MAX_SIZE=4G`. The cache is shared by this launcher's sessions and ignored by Git. |
| Shell isolation | Inherited `BB_*` variables are removed. The launcher sets its own game, data, config, patches, resolution, FPS, and logging paths/values. |

You can inspect the whole request with:

```sh
python3 play.py --metalfx --tuned --windowed --check
```

`runtime_env` reports what the launcher will pass, not proof that MetalFX ran.
The check creates no directories, writes no settings, and starts no process.
The same switches work with `--bbport-src /path/to/your/built/bbport-mac`.
Without `--metalfx`, your saved upscaler stays in charge. Without `--tuned`,
bbport keeps its usual pacing and memory defaults. The launcher does not rewrite
`bbport.ini`; bbport's own overlay can still save settings during play.

I kept the Bloodborne defaults at 1080p / 60 cap / perf 3 / fullscreen.
I did not copy DS3's address patches, import adapter, or `object_motion=0`:
those belong to its game-specific setup. The existing Bloodborne patches and
motion settings stay in charge. No generic `--env` or experimental engine
switches are added in this first step.

The new cache starts cold and may add compilation stalls on the first visit.
I leave the old Mesa cache and bbport's separate shader cache untouched.

## Engine experiments already present here

The three DS3 engine exports were already committed in Bloodborne before this
review. I left them unchanged:

| Patch | Evidence and limit |
| --- | --- |
| [macOS host import probe](../patches/bbport/host-import-probe-macos.patch) | Checks shared host-memory import through `VK_EXT_external_memory_host`. DS3's guide records a faster GPU read in a probe; that is not gameplay speed. |
| [Guest memory in place](../patches/bbport/guest-in-place-macos.patch) | Imports 256 MiB chunks of the runtime's backing memory. DS3's guide records a crash with `BB_GUEST_IN_PLACE=1`; disabling GPU command writes only passed a menu smoke check there. It stays off. |
| [MetalFX frame interpolation](../patches/bbport/metalfx-frame-interpolation.patch) | Adds `MTLFXFrameInterpolator`, requires macOS 26+ and a supported device, and gates it behind `BB_METALFX_INTERPOLATE=1`. DS3's guide records no generated gameplay frames. It stays off. |

Later local DS3 handoff notes report visible corruption with guest memory in
place, and equal rendered/presented frame counts in an interpolation run. I
have not repeated those runs. The current desktop engine is a separate
`bbport-mac-ds3-fps` worktree at `7ca0055`, with additional local changes, so
its full behavior is not reproduced by these three exported patches.

## What I checked and what comes next

The local launcher tests cover all four flag combinations, a read-only check,
saved-settings preservation, rejection of inherited experiment settings, and
passing the profile through a real fixture shell process in a source path
containing spaces. These tests do not launch the game or exercise the GPU.

My next step is an agreed short play check using copied saves and a separate
session folder. I need actual scaler activation in the engine log and a visual
check before calling MetalFX active. Compare the same warm-cache route with
and without each flag; check controls, sound, game speed, picture quality,
save/load, stalls, and crashes as well as frame times. A requested setting or
a higher cap is not a measured improvement. I have no new Bloodborne FPS
result from this work.
