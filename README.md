```text
Document:    Bloodborne on Mac
Version:     v2.4.0
Author:      Christopher Celaya
Contact:     https://github.com/while-basic
Date:        2026-10-12
SHA256:      495fbb74e84e86123355c54efae6221f7e2f4925d92c8f4713ad97807675e83a
Chain:       solana-mainnet
Tx:          23maDM8uzv3tGnSAoqywFPEdSYswicLWVMsEzzXiuiMaPVWXdLNUmjD9YFQtkVAGV4wKeGyHidE1dQxbRUF4fthe
License:     The Unlicense (public domain dedication)
```

# Bloodborne on Mac

I'm running Bloodborne on an **M5 Max with 128 GB of RAM**. Right now I'm getting
around **24–55 FPS**. I want to get that to **90+ FPS**, then work on Windows and
Linux, then see what I can do in a web browser.

I put this launcher together so other people can set up the same thing. It uses
[shadPS4](https://github.com/shadps4-emu/shadPS4) to run the game and applies the
resolution, FPS, and performance patches before launching.

**Want your agent to do the setup? [Copy one of these prompts.](docs/AGENT-INSTALL.md)**

This is a personal project. I'm [Christopher Celaya / while-basic](https://github.com/while-basic).
My code and docs are open source under [the Unlicense](LICENSE). Use them, change
them, fork them. I claim no ownership of Bloodborne, shadPS4, or anyone else's work.

## What you'll need

- A Mac with Python 3.11 or newer, shadPS4 Qt Launcher, and Rosetta for the
  x86_64 emulator.
- Your own extracted Bloodborne files: **CUSA00900, update 01.09**.
- The `Bloodborne.xml` patch file linked in the setup below.

If you own a PS4 and a disc or digital copy, start with the
[shadPS4 instructions](https://github.com/shadps4-emu/shadPS4) for dumping and
setting up your game. The launcher needs the extracted game folder; it can't
read a PS4 disc in a Mac drive or launch a PKG, ISO, or ZIP directly.

If you already downloaded your files, make sure you have the right to use that
copy. I don't include game files, updates, DLC, firmware, keys, saves, or game
download links here.

## My setup

| Part | What I'm using |
| --- | --- |
| Mac | MacBook Pro, Mac17,6 |
| Chip | Apple M5 Max |
| CPU | 18 cores: 6 Super + 12 Performance |
| GPU | 40 cores |
| Memory | 128 GB unified memory |
| macOS | 27.0, build 26A5406e |
| Python | 3.11.9 |
| Emulator | shadPS4 pre-release, x86_64 through Rosetta 2 |
| Graphics | Vulkan through KosmicKrisp / Metal |
| Game | CUSA00900, update 01.09 |
| FPS I'm seeing | 24–55 |

These are my specs, not minimum requirements. I haven't tested other Macs yet.
I also haven't written up a repeatable benchmark for that FPS range. That's
on [the roadmap](docs/ROADMAP.md).

The launcher starts at **1080p, a 60 FPS cap, perf 3, and borderless fullscreen**.
Those are the defaults, not a record of every setting used for the range above.

## Set it up

1. Install Python 3.11+ and
   [shadPS4 Qt Launcher](https://github.com/shadps4-emu/shadPS4-qtlauncher).
   Install Rosetta when macOS asks for it.
2. Install the pre-release engine through Qt Launcher. Open the emulator once,
   then close it so its config is saved. The script looks for:

   ```text
   ~/Library/Application Support/shadPS4QtLauncher/versions/Pre-release/shadps4
   ~/Library/Application Support/shadPS4/config.json
   ```

   If your install uses different paths or a different config format, the script
   will need an update.
3. Clone this repo:

   ```sh
   git clone https://github.com/while-basic/bloodborne.git
   cd bloodborne
   ```

4. Put your complete, extracted **CUSA00900 / 01.09** game folder here. Install
   the matching update using the upstream instructions first. Renaming a folder
   from another region won't make its patches compatible.

   ```text
   runtime/
     games/
       CUSA00900/
         eboot.bin
         ...the rest of your game files...
   ```

5. Download the patch file from the
   [shadPS4 patch collection](https://github.com/shadps4-emu/ps4_cheats/blob/main/PATCHES/Bloodborne.xml):

   ```sh
   mkdir -p runtime/downloads
   curl --fail --location \
     https://raw.githubusercontent.com/shadps4-emu/ps4_cheats/main/PATCHES/Bloodborne.xml \
     --output runtime/downloads/Bloodborne.xml
   ```

   The patch file can change upstream. The launcher checks patch names and
   versions, but it doesn't verify your game dump.
6. Close shadPS4, back up your saves, and check the setup:

   ```sh
   python3 play.py --check
   ```

   This checks local files and patches without launching or changing settings.
   You'll still need to launch the game to know it works.
7. Run it:

   ```sh
   python3 play.py
   ```

   You can also double-click `Play Bloodborne.command`. If you downloaded a ZIP
   and it won't open, run `chmod +x "Play Bloodborne.command"`.

## Try different settings

```sh
python3 play.py --help
python3 play.py --windowed
python3 play.py --resolution 1440p --fps 90 --perf 7
python3 play.py --extra "Disable AA" --check
python3 play.py --no-log
python3 play.py --resolution 720p             # 720p and 900p are there for testing, not for looks
python3 play.py --perf 4                      # shadows off: a few more FPS in crowds
python3 play.py --keep-facegen                # put Facegen back (see below)
python3 play.py --engine nightly-app --fullscreen-mode exclusive   # Game Mode experiment, read below first
```

You can choose 1080p, 1440p, or 4k, with a 60, 90, or 120 FPS cap. Setting the
cap to 90 doesn't make the game run at 90. I haven't tested every combination.

The performance levels build on each other. Level 0 keeps the base performance,
intro-skip, and FPS patches. Higher levels add these changes:

| Level | What it changes |
| --- | --- |
| 1 | Disables motion blur |
| 2 | Disables chromatic aberration |
| 3 — default | Lowers specific renders |
| 4 | Disables dynamic light shadows |
| 5 | Disables SSAO |
| 6 | Disables depth of field |
| 7 | Disables bloom |

You can repeat `--extra` for more patches. Use their exact names from the XML
and check that they work together.

For `--engine release`, put your separate emulator install at
`runtime/Bloodborne Emulator.app/Contents/MacOS/shadps4`.
The script also tries that path if it can't find the nightly. It doesn't
download or update the emulator for you.

## Backups and settings

The launcher backs up `config.json` to `runtime/config-backups/` before changing
the display settings, FPS counter, extra direct memory, pipeline cache, and logging.

It writes the selected patches to:

```text
~/Library/Application Support/shadPS4/patches/bloodborne-profile/
```

That profile stays there, so Qt Launcher can use it later too. Check for conflicts
if you have other Bloodborne patches enabled. Session logs go in
`runtime/sessions/`.

To undo a change, close shadPS4, restore the config backup you want, and remove
only the `bloodborne-profile` folder. **The script backs up config, not saves
or an older copy of that patch folder.** Back those up separately.

## Things that still need work

This launcher currently uses Mac paths and the CUSA00900 / 01.09 game profile.
Windows, Linux, other game regions, and browsers still need work.

Shader compilation can cause stutter when you enter an area. I've also seen a
graphics crash with the 0.19.0 emulator and occasional input or loading freezes.
Restarting the game may help.

Some earlier short test runs showed higher peaks than 24–55 FPS. I want to test
the same route on a fixed emulator build before putting out a proper benchmark.
For now, I'm using the range I'm seeing while playing.

### What I measured on October 12

I played with the DualShock while a script read the FPS counter off the screen every second or two.

| Profile | Where | median | slowest 10% | min | max |
| --- | --- | ---: | ---: | ---: | ---: |
| default (1080p, 60 cap, perf 3) | carriage fight, gate | 47 | 43 | 37 | 60 |
| default at 720p | bonfire mob | 53 | 48 | 37 | 60 |
| perf 7 + Model LOD 1 + 1080p Light Grid | standing at the gate | 51 | 43 | 43 | 49 |
| default | crowded fight until I died | 48 | 41 | 23 | 60 |

Those earlier route tests suggested a CPU limit: reducing the pixel count helped
only a little, and the game and graphics-command threads both did substantial
work. CPU/GPU utilization alone does not establish the cause of every slowdown,
or a guaranteed FPS floor in other scenes.

Later on October 12, a 900p boss attempt felt much worse than 1080p. I restored
1080p with the 60 FPS target and perf 3, and the next run felt very good. I did
not collect a new FPS number for that comparison. The working command, larger
FPS counter setting, and next-session notes are in [PERFORMANCE.md](PERFORMANCE.md).

Two other things from that session:

- The spiky-geometry glitch (characters exploding into shapes) is the known Facegen bug.
  `Disable Facegen` is now part of the default profile; `--keep-facegen` restores it.
- macOS Game Mode never turned on for a bare binary. It does turn on when the nightly is
  wrapped in an app bundle with a game category (`--engine nightly-app`) and run in
  exclusive fullscreen, but that window disappeared as soon as another app took focus, so
  I have no Game Mode numbers yet. The bundle lives under `runtime/` and is ignored by git.

[Here's what I want to work on next.](docs/ROADMAP.md)
If you try it, [send your specs and results](CONTRIBUTING.md).

## Credit where it's due

[shadPS4](https://github.com/shadps4-emu/shadPS4) does the emulation,
[Qt Launcher](https://github.com/shadps4-emu/shadPS4-qtlauncher) manages the engine,
and the [patch authors](https://github.com/shadps4-emu/ps4_cheats) made the game patches.
My part here is the launcher and setup.

My original code, tests, and docs—including earlier versions—are available under
[the Unlicense](LICENSE), without a warranty. The game, emulator, patches, and
their assets keep their own licenses and rights.
