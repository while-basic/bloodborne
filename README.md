```text
Document:    Bloodborne on Mac
Version:     v3.1.0
Author:      Christopher Celaya
Contact:     https://github.com/while-basic
Date:        2026-10-13
SHA256:      8163b4ad04afc42d2e1cdf8edb175d52dd839089fab6ff1b8d1c263630041bba
Chain:       solana-mainnet
Tx:          7pBAUqa8CEm4AhM59dSbp5Sb6sHT3qo91J7yYDsuTgsdcgnnS38CMWjnYAXzBx3Pajrm9fqEX27YepiAtki1cVJ
License:     The Unlicense (public domain dedication)
```

# Bloodborne on Mac 🩸

I put Bloodborne on my Mac. The hunt got a little out of hand.

More than **1 million people** have seen it running at **50+ FPS**. My next boss
is **90+ FPS**. The internet has questions. So do the villagers.

I'm [Christopher](https://github.com/while-basic). This is my small launcher for
[shadPS4](https://github.com/shadps4-emu/shadPS4), plus the steps I took to get
from my own PS4 disc to playing on my Mac. The shadPS4 team built the emulator.
I built this setup around it, with help from Codex and Claude.

**Start here: [the guided PS4-to-Mac tutorial](docs/PS4-TO-MAC.md).**
Already have your game files? Jump to [Mac setup](#mac-setup).
Want an agent to help? [Copy a starter prompt](docs/AGENT-INSTALL.md).

## Where I'm at

The shared footage shows 50+ FPS. My earlier play sessions ranged from about
24–55 FPS, with some quiet spots near 60. Busy fights can dip. I have **not**
reached steady 90+ FPS yet. A million views do not add a million frames.

My current starting point is **1080p, a 60 FPS cap, perf 3, and borderless
fullscreen**. I tried 900p during a boss fight, found it much worse, and went
back to 1080p. The restored run felt very good; I did not measure new FPS for it.
See [my performance notes](PERFORMANCE.md) for the test limits.

## Done, next, and a slightly wild idea

- [x] Start with my own Bloodborne disc and a PS4.
- [x] Get homebrew running on my PS4 11.02.
- [x] Use a USB-C Ethernet adapter and cable for my local setup and transfers.
- [x] Back up my game and get CUSA00900 / update 01.09 running on my Mac.
- [x] Add a one-command launcher and a check that changes no settings.
- [x] Add resolution, FPS, and visual-effect patches.
- [x] Turn on the shader pipeline cache and stop log writes blocking game threads.
- [x] Disable Facegen by default to avoid the spiky-character bug.
- [x] Add config backups, private session logs, and a light CPU/GPU recorder.
- [x] Share steps and prompts for Codex and Claude.
- [x] Add an optional frame logger and analyzer for local emulator builds.
- [ ] Measure the same route across several runs and reach **90+ FPS on Mac**.
- [ ] Bring this launcher to Windows and Linux.
- [ ] Explore a browser version. Local play or streaming? Still an open idea.

The longer plan is in [my roadmap](docs/ROADMAP.md). Checked boxes describe what
I've done; they are not a promise that every Mac or PS4 will work the same way.

## Tutorial: let Codex or Claude walk with you

My path was: **disc → PS4 homebrew → my game backup → shadPS4 → this launcher**.
An agent handled the Mac commands and talked me through the PS4 steps.
I still pressed the controller buttons and checked what the PS4 showed.

1. **Tell the agent what you have.** Mac model, memory, PS4 firmware, disc or
   digital copy, controller, USB drive, Ethernet cable, and any USB-C adapter.
2. **Ask before testing the Mac.** The agent should request permission for a
   local performance test. It should explain the load and length first.
   Reading specs is a first check; playing the game is the real test.
3. **Keep the PS4 firmware where it is.** Check for a queued system update in
   Notifications / Downloads. Identify that exact item before deleting it.
   Do not delete game updates or saves. Then turn off automatic system downloads.
4. **Pick the right homebrew path.** Check the exact firmware against the
   chosen tool's current guide. “All 13.xx and below” is too broad.
5. **Choose USB or Ethernet for each job.** A USB drive can carry a homebrew
   package. Ethernet can host a browser loader and move files. An Ethernet
   cable alone does not make every firmware support the same jailbreak.
6. **Install homebrew, back up your own game, and set up the Mac.** Follow the
   [full walkthrough](docs/PS4-TO-MAC.md), with checks at each step.

I used **PS4 11.02 with a CSSFontFace/Lapse browser loader**. Other published
routes cover specific versions through **13.00**, but that does not verify
every 13.xx release. I checked the linked project guides on October 13, 2026.
The [firmware table and sources](docs/PS4-TO-MAC.md#3-pick-a-firmware-path) show
the limits. Stay on your current firmware while you check.

## My Mac

| Part | My setup |
| --- | --- |
| Mac | MacBook Pro with Apple M5 Max |
| CPU / GPU | 18 CPU cores / 40 GPU cores |
| Memory | 128 GB |
| macOS | 27.0 |
| Emulator | shadPS4 pre-release, x86-64 through Rosetta |
| Graphics | Vulkan through KosmicKrisp and Metal |
| Game | CUSA00900, update 01.09 |

These are my specs, not minimum requirements. Check the
[current shadPS4 Mac requirements](https://github.com/shadps4-emu/shadPS4/blob/main/documents/building-macos.md)
before you buy hardware. More than 60 visible frames also needs a display
running above 60 Hz.

## Mac setup

I use **Python 3.11+**, the
[shadPS4 Qt Launcher](https://github.com/shadps4-emu/shadPS4-qtlauncher), Rosetta,
and my own complete, extracted **CUSA00900 / 01.09** game folder.
A PS4 disc in a Mac drive will not work. This script cannot launch a PKG, ZIP,
or ISO directly. Use [shadPS4's setup guides](https://shadps4.net/) for dumping
and importing your own files.

1. Install the pre-release engine through Qt Launcher. Open it once and close
   it to create its settings. This wrapper expects these paths:

   ```text
   ~/Library/Application Support/shadPS4QtLauncher/versions/Pre-release/shadps4
   ~/Library/Application Support/shadPS4/config.json
   ```

2. Clone this repo:

   ```sh
   git clone https://github.com/while-basic/bloodborne.git
   cd bloodborne
   ```

3. Put the complete extracted game here, with the matching update already
   installed. Keep your original backup. Changing a folder name does not
   change the game's region.

   ```text
   runtime/games/CUSA00900/eboot.bin
   runtime/games/CUSA00900/...the rest of the game...
   ```

4. Get the patches from the
   [shadPS4 patch collection](https://github.com/shadps4-emu/ps4_cheats/blob/main/PATCHES/Bloodborne.xml):

   ```sh
   mkdir -p runtime/downloads
   curl --fail --location \
     https://raw.githubusercontent.com/shadps4-emu/ps4_cheats/main/PATCHES/Bloodborne.xml \
     --output runtime/downloads/Bloodborne.xml
   ```

5. Close shadPS4. Back up your saves and any existing generated patch profile.
   Then check the local files without launching or changing settings:

   ```sh
   python3 play.py --check
   ```

6. Launch:

   ```sh
   python3 play.py
   ```

   Or double-click `Play Bloodborne.command`. For a ZIP download, you may need
   `chmod +x "Play Bloodborne.command"` first. Confirm the title screen, then
   check controls, sound, and actual play. A passing file check is only step one.

## Turn the knobs

```sh
python3 play.py --help
python3 play.py --windowed
python3 play.py --fps 90 --check
python3 play.py --resolution 1440p --fps 90 --perf 4
python3 play.py --extra "Disable AA" --check
python3 play.py --no-log
python3 play.py --keep-facegen
python3 play.py --keep-vulkan-validation  # debugging only; slower
```

I support 720p, 900p, 1080p, 1440p, and 4K, with 60, 90, or 120 FPS caps.
These are choices to test. **A 90 FPS cap does not create 90 FPS.**
Keep 720p and 900p as experiments; my current baseline is 1080p.

The launcher turns Vulkan core validation off for play. It adds checks to many
graphics calls and can cost a lot of speed. Use `--keep-vulkan-validation` only
when I am chasing an emulator bug.

| Perf level | Added change |
| --- | --- |
| 0 | Base performance patch, intro skip, FPS patch, and Facegen fix |
| 1 | No motion blur |
| 2 | No chromatic aberration |
| 3 — default | Lower some extra renders |
| 4 | No dynamic light shadows |
| 5 | No SSAO |
| 6 | No depth of field |
| 7 | No bloom |

Each level includes the ones above it. Higher levels change the picture.
`--keep-facegen` removes the Facegen fix at any level. Repeat `--extra` to add
named XML patches, and check for conflicts.

`--engine release` uses a separate install at
`runtime/Bloodborne Emulator.app/Contents/MacOS/shadps4`.
`--engine nightly-app` expects a separately prepared `Bloodborne Nightly.app`
at the same level. That game-category app bundle can enable macOS Game Mode
in exclusive fullscreen. The launcher does not create it, and I have no
measured Game Mode speedup to share.

## Backups and the way home

I save a copy of `config.json` in `runtime/config-backups/` before changing it.
The launcher writes patches to
`~/Library/Application Support/shadPS4/patches/bloodborne-profile/` and keeps
session logs in `runtime/sessions/`. The profile also stays active in Qt Launcher.

To undo a profile change, close shadPS4, restore your chosen config backup,
and restore your prior `bloodborne-profile` folder, or remove that folder if
there was none before. **Automatic backups cover config only.** Save files
and older patch profiles need their own backup.

I've seen shader stutter, graphics crashes, and input or loading freezes.
Keep a working emulator build and change one thing at a time. See
[troubleshooting prompts](docs/AGENT-INSTALL.md) and [performance notes](PERFORMANCE.md).

## Credits and sharing

Thanks to [shadPS4](https://github.com/shadps4-emu/shadPS4),
[the patch authors](https://github.com/shadps4-emu/ps4_cheats),
[GoldHEN](https://github.com/GoldHEN/GoldHEN), and the homebrew developers whose
work made this possible. Bloodborne belongs to its rights holders.

My original code and docs use [the Unlicense](LICENSE). Fork away.
I do not include game data, firmware, keys, saves, or emulator bundles.
Want to help hunt frames? [Here's how to contribute](CONTRIBUTING.md),
including [how I capture frame times](docs/FRAME-CAPTURE.md).
