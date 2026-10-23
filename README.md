```text
Document:    Bloodborne on Mac
Version:     v4.1.0
Author:      Christopher Celaya
Contact:     https://github.com/while-basic
Date:        2026-10-22
SHA256:      ebbf71576a73420274188a7f3ccfa3594e030f2d25b6a14fb7d23946a6082d00
Chain:       solana-mainnet
Tx:          XkyjZU77Ep3bTe24LVtPefyZyiYnH9QBwvKLVKPSLRhWpgBjVjzQRxwrtqSXx7jf4zxSuGNvNmu3NejCNgZzHfe
License:     The Unlicense (public domain dedication)
```

# Bloodborne on Mac 🩸

I put Bloodborne on my Mac. The hunt got a little out of hand.

More than **1 million people** have seen my earlier **50+ FPS** footage.
Now this repo runs **[bbport for Mac](https://github.com/bmy/bbport-mac)**.
One game, one launcher, fewer things to trip over on the way to Yharnam.

I'm [Christopher](https://github.com/while-basic). I made this small launcher,
the setup guide, and a few optional patches. The bbport developers did the
hard work that makes the game run. I started with my own PS4 disc and had
Codex and Claude help with the Mac commands.

**Start here: [the guided PS4-to-Mac tutorial](docs/PS4-TO-MAC.md).**
Already have your extracted game? Jump to [Mac setup](#mac-setup).
Want an AI helper to do the typing? [Copy a starter prompt](docs/AGENT-INSTALL.md).

## What this is, in plain words

Bloodborne was made for PS4. **bbport** is a community project that runs the
original game code on a computer. [The Mac port](https://github.com/bmy/bbport-mac)
brings that work to Apple Silicon. This repo puts a small launcher around it.
It is not an official PC release, and it does not contain the game.

You bring your own complete, decrypted game backup and matching update.
A PS4 disc in a Mac drive will not work. This script cannot open a PKG, ZIP,
or ISO game file either.

A few words that come up a lot:

| Word | What it means |
| --- | --- |
| **FPS** | Frames per second. 30 looks OK. 60 looks smooth. |
| **Frame time** | How long one picture takes. Big spikes feel like stutter. |
| **Dump** | A usable backup made from your own console and game. |
| **Patch** | A small change, like turning off motion blur. |
| **Rosetta** | Apple's helper for running Intel code on an Apple Silicon Mac. |
| **Shader** | A little graphics program. Building these can slow the first visit to an area. |

## Where I'm at

At the same Central Yharnam lamp, my first bbport test held **56–59 FPS**.
My later crowd session felt smoother and logged a **60 FPS median**, with
some long hitches. That is one session, not a promise of a steady 60 everywhere.
The dates and limits are in [my performance notes](PERFORMANCE.md).

My next boss is **steady 60+ FPS in busy fights**, then **90+**.
A million views do not add a million frames. I only share numbers I measured.

The starting settings are **1080p / 60 FPS cap / perf 3 / fullscreen**.
bbport is still experimental. Some effects are missing on Mac, objects can
pop in, and busy scenes can slow down. Keep a good save backup.

## My Mac

| Part | My setup |
| --- | --- |
| Mac | MacBook Pro with Apple M5 Max |
| CPU / GPU | 18 CPU cores / 40 GPU cores |
| Memory | 128 GB |
| macOS | 27.0 |
| Engine | bbport for Mac, pinned release 0.4-v1 |
| Graphics | Vulkan through KosmicKrisp and Metal |
| Game | CUSA00900, update 01.09 |

These are my specs, not minimum requirements. The pinned
[Mac port guide](https://github.com/bmy/bbport-mac/tree/0.4-v1) calls for
Apple Silicon, macOS 26 or newer, and Rosetta 2. Check its current advice
before buying anything. My wrapper targets **CUSA00900 / 01.09**; upstream's
guide uses CUSA03173. Renaming another region's folder does not convert it.

## Mac setup

You'll use **Terminal** for a few commands. Copy one at a time, or let the
[setup prompt](docs/AGENT-INSTALL.md#i-already-have-my-extracted-game) help.
You need **Python 3.11 or newer**, Rosetta 2, and your own extracted game.

1. **Get this repo:**

   ```sh
   git clone https://github.com/while-basic/bloodborne.git
   cd bloodborne
   ```

2. **Install bbport:**

   ```sh
   python3 play.py --install
   ```

   This downloads the pinned official Mac release and checks its SHA-256
   fingerprint before unpacking it. Everything stays in `runtime/`.
   Nothing is installed into Applications. Follow the upstream Rosetta
   instructions and any normal macOS prompts; don't bypass security warnings.

3. **Put your game in place.** Keep your original backup safe.
   If your base game and update are separate, use this layout:

   ```text
   runtime/games/CUSA00900/eboot.bin
   runtime/games/CUSA00900/...the rest of the base game...
   runtime/games/CUSA00900-patch/eboot.bin
   runtime/games/CUSA00900-patch/...the rest of update 1.09...
   ```

   On the first launch, I make an APFS clone and lay the update over it.
   The originals stay put. This needs an APFS destination with room for changes.
   Already have the complete merged 1.09 game? Put it directly in
   `runtime/games/CUSA00900-109/`, with `eboot.bin` at the top.

4. **Check the files:**

   ```sh
   python3 play.py --check
   ```

   This changes nothing and does not launch the game. It checks the engine
   and game paths, then shows the launch settings. `merge_needed: true` means
   the first launch still needs to combine the base game and update.
   It does not prove the whole dump is valid or that gameplay works.

5. **Play:**

   ```sh
   python3 play.py
   ```

   Or double-click `Play Bloodborne.command`. If you downloaded a ZIP, run
   `chmod +x "Play Bloodborne.command"` once first.
   The first launch can sit on a black screen while shaders build.
   Check the title screen, controls, sound, and a short walk.
   Space is Cross on the keyboard; a controller works too.

## Turn the knobs

```sh
python3 play.py --help
python3 play.py --windowed
python3 play.py --perf 4
python3 play.py --resolution 1440p --fps 90 --perf 4
python3 play.py --extra "Disable AA" --check
python3 play.py --no-log
python3 play.py --stats
```

I also brought over the first launcher settings from my DS3 project:

```sh
python3 play.py --metalfx --tuned --windowed --check
python3 play.py --metalfx --tuned --windowed
```

`--metalfx` requests MetalFX Native AA at your chosen resolution. `--tuned`
tries DS3's staging buffer, write-fault window, unpaced vblank, and Retina
settings. Both are optional; I have not measured them in Bloodborne. My usual
1080p / 60 cap / perf 3 setup stays the default. See the [Metal comparison](docs/METAL.md)
for the exact settings and what still needs a play check.

The launcher now ignores inherited `BB_*` shell variables. Use its flags and
your saved bbport settings. I pin Mesa's shader cache to `runtime/cache/mesa`
with a 4 GB limit; its first run may need to rebuild shaders. Existing caches
stay in place. `--check` shows the requested environment without writing files.

Resolution choices are 720p, 900p, 1080p, 1440p, and 4K. FPS caps are 60 or 90.
**A 90 FPS cap does not create 90 FPS.** A faster display is needed to show
more than 60 distinct frames each second. My way home stays 1080p.

The effects presets keep their existing numbers:

| Perf level | Effects turned off |
| --- | --- |
| 0 | No extra effects patches |
| 1 | Motion blur |
| 2–3 — default 3 | Motion blur and color fringing |
| 4 | All of those, plus dynamic light shadows |
| 5 | All of those, plus soft corner shadows (SSAO) |
| 6–7 | All of those, plus depth of field |

Extra patch names must match bbport's own patch file. A successful `--check`
prints your request; bbport checks those extra names when it launches.
`--no-log` skips the frame CSV. Basic diagnostic logs still exist.
`--stats` reads the latest frame CSV; [here is how to read it](docs/FRAME-CAPTURE.md).

## Saves and a way home

bbport keeps this launcher's settings, saves, caches, and logs under
`runtime/bbport/`. Save data is under `user/savedata/1/CUSA00900/` inside it.
Close the game before backing up or restoring that folder.

Existing bbport saves stay where they are. The launcher no longer imports
another app's saves automatically or changes another app's settings.
Keep any older installs and backups until you've checked your bbport save.
The engine is downloaded separately; updating this repo does not replace it.

## A few optional experiments

I also made a small [CSR mod](mods/csr/README.md): **Yharnam Can Opener**,
**Eviction Notice**, and **Gentleman’s Disagreement**, with a quiet CSR label
on the loading screens. The repo has the tools, not the edited game files.
The names and menu files pass local checks. In-game appearance still needs a
visual check. The normal launcher does not apply the mod automatically.

### My bbport patches

The pinned release can stop mid-fight with `Unknown data_format=15`.
My optional patch uses a stand-in for that draw instead of stopping the game.
It builds, but a long play test still needs to prove it.

```sh
git clone --recursive --branch 0.4-v1 https://github.com/bmy/bbport-mac ~/Documents/bbport-mac
cd ~/Documents/bbport-mac
git apply /path/to/bloodborne/patches/bbport/vertex-format-standin.patch
bash tools/macos/setup_deps.sh
bash tools/macos/build.sh
cd /path/to/bloodborne
python3 play.py --bbport-src ~/Documents/bbport-mac
```

Streaming or recording? Apply `patches/bbport/big-fps-counter.patch` before
building too, then add `--fps-size 3`. Bigger numbers do not make bigger FPS.

## Credits and sharing

Thanks to [bbport](https://github.com/deadinside28/bloodborne_pc),
[bbport for Mac](https://github.com/bmy/bbport-mac),
[shadPS4](https://github.com/shadps4-emu/shadPS4) for the renderer and shader
work bbport builds on, [KosmicKrisp](https://github.com/shadexternals/mesa-kosmickrisp),
[the community patch authors](https://github.com/shadps4-emu/ps4_cheats),
[GoldHEN](https://github.com/GoldHEN/GoldHEN), and the homebrew developers
who made my backup possible. Bloodborne belongs to its rights holders.

My original code and docs use [the Unlicense](LICENSE). Fork away.
The bbport patches keep their upstream GPL terms; [the license notes](docs/LICENSE-NOTES.md)
spell that out. I do not include game data, firmware, keys, saves, or engine
bundles. Please don't ask me for them.

Want to help hunt frames? [Here's how to contribute](CONTRIBUTING.md).
[The roadmap](docs/ROADMAP.md) has the next fights, including Windows and Linux.
