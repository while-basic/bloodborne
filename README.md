```text
Document:    Bloodborne on Mac — Public Launcher Guide
Version:     v2.1.0
Author:      Christopher Celaya
Contact:     https://github.com/while-basic
Date:        2026-10-12
SHA256:      cf6672e7171125fc2035977988c3a4d1e96d6875e17e61eadb040bf78032a857
Chain:       solana-mainnet
Tx:          4TFuyD98c8APk2h4qcT3m3kCT1mTtqmrD7y6TAZ5GbxuK9iv6eAJS1pppbUZumo68M7A2PEJmLT1nP8LN3eYhquw
License:     The Unlicense (public domain dedication)
```

# Bloodborne on Mac

A small Python launcher that applies a display and performance patch profile, then
starts [shadPS4](https://github.com/shadps4-emu/shadPS4) with your local copy of Bloodborne.

An **open-source personal project** by [Christopher Celaya (@while-basic)](https://github.com/while-basic),
released under [the Unlicense](LICENSE). Use, copy, change, and share my original
code and docs freely. I claim no exclusive rights to this contribution and no
ownership of Bloodborne, shadPS4, or their assets.

**Let your agent install it:** copy a prompt from [Agent installation prompts](docs/AGENT-INSTALL.md).

**Current performance: 24–55 FPS on an M5 Max with 128 GB memory.**
The next goal is **90+ FPS on Mac**, followed by Windows and Linux optimization,
then browser research. These are plans, not supported features or promised results.

This repository contains launcher source and documentation only. It is an independent
community project, not affiliated with Sony, FromSoftware, or the shadPS4 team.

## Bring your own game

You must supply game files you are entitled to use. For disc or digital PS4 owners,
follow the [official shadPS4 documentation](https://github.com/shadps4-emu/shadPS4)
for compatible console, dumping, firmware, and installation requirements.

A PS4 or physical disc alone does not provide the extracted files this launcher needs.
It cannot read a PS4 disc in a Mac drive or launch a ZIP, PKG, or ISO directly.
If your files came from an internet download, you still need lawful rights to use
that copy; owning a disc does not automatically grant rights to every download.

**No game files, updates, DLC, console firmware, keys, saves, emulator binaries, or
game download links are included.** Do not commit or attach those files to issues.

## Tested system

Hardware and software below were read from the local test Mac on October 12, 2026.
The FPS range is the owner's report, not a fresh benchmark performed for this release.

| Item | Test system |
| --- | --- |
| Computer | MacBook Pro, model identifier Mac17,6 |
| Chip | Apple M5 Max |
| CPU | 18 cores: 6 Super + 12 Performance (macOS-reported labels) |
| GPU | 40 cores |
| Memory | 128 GB unified memory |
| macOS | 27.0, build 26A5406e |
| Python | 3.11.9; standard library only |
| Emulator | shadPS4 pre-release, x86_64 executable under Rosetta 2 |
| Graphics path | Vulkan through KosmicKrisp/Metal in the local emulator package |
| Game profile | Bloodborne CUSA00900, update 01.09 |
| Current gameplay | Owner reports 24–55 FPS |
| Launcher defaults | 1920 × 1080, 60 FPS cap, performance level 3, borderless fullscreen |

This is a **tested configuration, not a minimum requirement**. Other Macs, chip
variants, memory sizes, and macOS versions have not been qualified here.
The exact emulator revision and the scene, resolution, and settings behind the
24–55 FPS report still need to be recorded. Defaults above are not a claim about
the settings used for that report. See [the benchmark plan](docs/ROADMAP.md).

## macOS setup

1. Install Python 3.11 or newer and a macOS build of
   [shadPS4 Qt Launcher](https://github.com/shadps4-emu/shadPS4-qtlauncher).
   This project was checked with Python 3.11.9. Install Rosetta when macOS requests
   it for the x86_64 emulator.
2. Use Qt Launcher to install the pre-release engine. Open the emulator once and
   close it so its settings exist. The current script expects these default paths:

   ```text
   ~/Library/Application Support/shadPS4QtLauncher/versions/Pre-release/shadps4
   ~/Library/Application Support/shadPS4/config.json
   ```

   If your release uses different paths or a different config format, it needs a
   launcher update; arbitrary installations are not detected automatically.
3. Clone this repository or extract its source ZIP. Open a terminal in that folder:

   ```sh
   git clone https://github.com/while-basic/bloodborne.git
   cd bloodborne
   ```

   Put your own extracted **CUSA00900, version 01.09** game at the layout below.
   Install/merge the matching update using the upstream instructions first.
   Do not just rename another region's folder: patch compatibility is version-specific.
4. Obtain `Bloodborne.xml` from the upstream
   [shadPS4 patch collection](https://github.com/shadps4-emu/ps4_cheats/blob/main/PATCHES/Bloodborne.xml)
   and save it locally. It is a third-party dependency, not bundled here:

   ```sh
   mkdir -p runtime/downloads runtime/games
   curl --fail --location \
     https://raw.githubusercontent.com/shadps4-emu/ps4_cheats/main/PATCHES/Bloodborne.xml \
     --output runtime/downloads/Bloodborne.xml
   ```

   The upstream branch can change. This launcher checks selected patch names and
   their game version; it does not authenticate or validate your game dump.
5. Keep the complete extracted game directory, not just its executable:

   ```text
   runtime/
     downloads/
       Bloodborne.xml
     games/
       CUSA00900/
         eboot.bin
         ...the rest of your extracted, updated game...
   ```
6. Quit all running shadPS4 sessions. Back up your saves with the emulator's tools,
   then validate the local paths and patch selection:

   ```sh
   python3 play.py --check
   ```

   A successful check does **not** prove that the game boots or runs correctly.
   It does not launch the emulator or change settings.
7. Launch:

   ```sh
   python3 play.py
   ```

   You can also double-click `Play Bloodborne.command`. If its executable bit was
   lost when extracting a ZIP, use `chmod +x "Play Bloodborne.command"`.

## Profiles and controls

```sh
python3 play.py --help
python3 play.py --windowed
python3 play.py --resolution 1440p --fps 90 --perf 7
python3 play.py --extra "Disable AA" --check
python3 play.py --no-log
```

Resolution options are 1080p, 1440p, and 4k. FPS caps are 60, 90, and 120.
**Selecting 90 or 120 does not mean the game reaches that speed.**
4k and non-default combinations have no public qualification claim here.

Performance level 0 enables the base performance, intro-skip, and FPS patches.
Each higher level adds the next change; effects may look different:

| Level | Added change |
| --- | --- |
| 1 | Disable motion blur |
| 2 | Disable chromatic aberration |
| 3 (default) | Lower specific renders |
| 4 | Disable dynamic light shadows |
| 5 | Disable SSAO |
| 6 | Disable depth of field |
| 7 | Disable bloom |

`--extra` can be repeated and must match an upstream XML patch name exactly.
Do not combine arbitrary patches without checking their compatibility.

`--engine release` expects your separately installed emulator at
`runtime/Bloodborne Emulator.app/Contents/MacOS/shadps4`.
If the nightly executable is missing, the launcher tries that same fallback.
There is no automatic emulator download or update.

## What the launcher changes

Launching backs up `config.json` into `runtime/config-backups/`, then updates
resolution, fullscreen mode, vblank frequency, extra direct memory, the FPS
counter, pipeline caching, and logging. It installs its selected patches into:

```text
~/Library/Application Support/shadPS4/patches/bloodborne-profile/
```

That profile persists and can also affect later launches through Qt Launcher.
Other enabled Bloodborne patch profiles may conflict; review them in the emulator.
Logs go into `runtime/sessions/`. Runtime files stay outside Git.

To undo the settings change, quit shadPS4, copy the desired backup over its
`config.json`, and remove only the `bloodborne-profile` patch folder.
Do not remove your other emulator data. The script does not back up saves or
restore a previous copy of its patch folder.

## Known limits

- This wrapper currently supports macOS paths only. Upstream shadPS4 support on
  other operating systems is separate from support in this wrapper.
- Only the CUSA00900 / 01.09 profile is configured. Other game regions need validation
  and a code change.
- Shader compilation may cause stutter, especially on first visits to an area.
- Earlier local testing saw a graphics crash in the 0.19.0 emulator and occasional
  input or idle/loading freezes. Quit and restart if affected.
- A prior README contained short OCR-sampled runs with higher peaks than the
  current 24–55 FPS report. Those runs are not a repeatable public benchmark.
  A fresh benchmark with a fixed route and exact build IDs is planned.
- There is no browser build, browser streaming setup, or 90+ FPS release yet.

Read [the roadmap](docs/ROADMAP.md) for the planned order and
[contribution notes](CONTRIBUTING.md) for local checks and useful bug reports.

## Credits and license

Emulation is provided by [shadPS4](https://github.com/shadps4-emu/shadPS4);
engine management by [Qt Launcher](https://github.com/shadps4-emu/shadPS4-qtlauncher);
game patches by the [upstream patch authors](https://github.com/shadps4-emu/ps4_cheats).
Each external project retains its own license. No ownership of those projects or
Bloodborne is claimed.

My original launcher code, tests, and documentation are open source under
[the Unlicense](LICENSE), a public-domain dedication with a fallback permission
grant where needed. This applies to my contributions in this repository,
including earlier revisions of those contributions. No warranty is provided.
The game, emulator, third-party patches, and their assets keep their own rights
and licenses; this dedication cannot grant rights to someone else's work.
