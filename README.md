```text
Document:    Bloodborne on Mac
Version:     v3.5.0
Author:      Christopher Celaya
Contact:     https://github.com/while-basic
Date:        2026-10-14
SHA256:      e8d300ee09dd816c3ea84be980978c11d2470223a4fd497e99f88a1e9ba4dbda
Chain:       solana-mainnet
Tx:          2xweiW8w5siBF6PEj7KzL6ptygjw9eC8SSQc6sawU2PWqGD4ZSzwim51THqH3Uwpm99Sx7zBAGgNJYqkcHYebA2C
License:     The Unlicense (public domain dedication)
```

# Bloodborne on Mac 🩸

I put Bloodborne on my Mac. The hunt got a little out of hand.

More than **1 million people** have seen it running at **50+ FPS**. My next boss
is **60+ FPS in the busiest fights**. The internet has questions. So do the villagers.

I'm [Christopher](https://github.com/while-basic). This is my small launcher for
[shadPS4](https://github.com/shadps4-emu/shadPS4), plus the steps I took to get
from my own PS4 disc to playing on my Mac. The shadPS4 team built the emulator.
I built this setup around it, with help from Codex and Claude.

**Start here: [the guided PS4-to-Mac tutorial](docs/PS4-TO-MAC.md).**
Already have your game files? Jump to [Mac setup](#mac-setup).
Want an AI helper to do the typing? [Copy a starter prompt](docs/AGENT-INSTALL.md).

## What is this, in plain words?

Bloodborne only came out on PS4. A Mac can't play PS4 discs.

So I used an **emulator**: a program that pretends to be a PS4, so the game
thinks it's home. The emulator I use is called **shadPS4**. It's free and made
by volunteers.

The emulator needs a copy of the game's files. I made that copy from **my own
disc on my own PS4**. That took a few steps, and the tutorial walks you through
each one. This repo has no game files. You bring your own copy.

My part is the small launcher script. It starts the emulator with the right
settings, so you don't have to set fifty switches by hand.

A few words you'll see a lot:

| Word | What it means |
| --- | --- |
| **FPS** | Frames per second. How many pictures the screen shows each second. 30 looks OK. 60 looks smooth. |
| **Emulator** | A program that acts like a game console on your computer. |
| **Firmware** | The PS4's own system software. Its version number matters a lot. |
| **Homebrew** | Unofficial apps you can run on a PS4. I used them to copy my own game. |
| **Dump** | A copy of your game's files, taken from your own console. |
| **Patch** | A small change to the game, like "turn off motion blur" or "allow 60 FPS". |
| **Terminal** | The Mac app where you type commands. It lives in Applications → Utilities. |

## Where I'm at

The shared footage shows 50+ FPS. In quiet places I hit about 60. When a crowd
of villagers shows up, my Mac drops to about **40–48 FPS**. That's still playable,
but you can feel it.

I tested why. The slow part isn't the graphics chip. It's the Mac's processor
pretending to be a PS4 processor, one game step at a time. Lowering the picture
quality barely helps in crowds. I wrote it all down in
[my performance notes](PERFORMANCE.md).

My best setting right now is **1080p, a 60 FPS cap, perf 3, and borderless
fullscreen**. That's what the launcher picks for you.

**New: a faster engine.** The launcher can now also run
[bbport for Mac](https://github.com/bmy/bbport-mac), a Bloodborne-only engine
built on shadPS4's parts. At the same Central Yharnam spot where shadPS4 gave
me 43–48 FPS, bbport held **56–59**. I haven't measured the big crowd on it yet.
That's the next fight. [How to try it](#try-the-faster-engine-bbport).

A million views do not add a million frames. I only share numbers I measured.

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
- [ ] Hold **60+ FPS in the busiest crowds** on my Mac.
- [ ] Then chase **90+ FPS**.
- [ ] Bring this setup to Windows and Linux ([my plan](docs/WINDOWS-LINUX.md)).
- [ ] Explore a browser version. Local play or streaming? Still an open idea.

The longer plan is in [my roadmap](docs/ROADMAP.md). Checked boxes describe what
I've done; they are not a promise that every Mac or PS4 will work the same way.

## Tutorial: let Codex or Claude walk with you

My path was: **disc → PS4 homebrew → my game backup → shadPS4 → this launcher**.

You don't need to know how to code. I used an AI helper (Codex or Claude) that
can type commands on my Mac. It handled the Mac side and talked me through the
PS4 screens. I still pressed the controller buttons and told it what the PS4 showed.

1. **Tell the helper what you have.** Your Mac model, memory, PS4 firmware
   number, disc or digital copy, controller, USB drive, Ethernet cable, and
   any USB-C adapter.
2. **Let it ask before testing your Mac.** A speed test makes the fans work.
   The helper should tell you how long it takes first. You can say no.
3. **Don't update your PS4.** A newer firmware can close the door for good.
   Check Notifications / Downloads for a waiting system update. Make sure it's
   the system update before you delete it. Leave game updates and saves alone.
   Then turn off automatic system downloads.
4. **Pick the right homebrew path for your firmware.** Each tool works on
   certain firmware numbers only. "All 13.xx and below" is too broad. Check the
   exact number against the tool's own guide.
5. **Choose USB or Ethernet for each job.** A USB drive can carry an app to
   install. An Ethernet cable can connect the PS4 straight to your Mac.
   A cable doesn't make every firmware work the same way.
6. **Install homebrew, back up your own game, and set up the Mac.** Follow the
   [full walkthrough](docs/PS4-TO-MAC.md). It has a check at each step.

I used **PS4 11.02 with a CSSFontFace/Lapse browser loader**. Other published
routes cover specific versions through **13.00**, but that does not cover
every 13.xx release. I checked the linked project guides on October 13, 2026.
The [firmware table and sources](docs/PS4-TO-MAC.md#3-check-the-exact-firmware-path)
show the limits. Stay on your current firmware while you check.

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

These are my specs, not minimum requirements. It needs an Apple Silicon Mac
(M1 or newer). A slower chip means fewer frames. Check the
[current shadPS4 Mac requirements](https://github.com/shadps4-emu/shadPS4/blob/main/documents/building-macos.md)
before you buy anything. More than 60 visible frames also needs a screen
that runs above 60 Hz.

## Mac setup

You'll type a few commands in **Terminal**. Copy and paste them one at a time.
Or paste [the setup prompt](docs/AGENT-INSTALL.md#i-already-have-my-extracted-game)
into Codex or Claude and let it do the typing.

You need:

- **Python 3.11 or newer.** Type `python3 --version` in Terminal to check.
- The [shadPS4 Qt Launcher](https://github.com/shadps4-emu/shadPS4-qtlauncher).
- **Rosetta**, Apple's helper for older apps. macOS offers to install it the
  first time it's needed.
- Your own complete, extracted **CUSA00900 / 01.09** game folder (the US game
  with update 1.09).

A PS4 disc in a Mac drive will not work. This script can't open a PKG, ZIP, or
ISO file either. Use [shadPS4's setup guides](https://shadps4.net/) to dump and
import your own files first.

1. **Install the emulator.** In Qt Launcher, install the pre-release engine.
   Open it once and close it, so it makes its settings files. The launcher
   looks for them here:

   ```text
   ~/Library/Application Support/shadPS4QtLauncher/versions/Pre-release/shadps4
   ~/Library/Application Support/shadPS4/config.json
   ```

2. **Download this repo:**

   ```sh
   git clone https://github.com/while-basic/bloodborne.git
   cd bloodborne
   ```

3. **Put your game in place.** Copy the whole extracted game here, with update
   1.09 already installed. Keep your original copy safe somewhere else.
   Renaming a folder does not change the game's region.

   ```text
   runtime/games/CUSA00900/eboot.bin
   runtime/games/CUSA00900/...the rest of the game...
   ```

4. **Get the patches** from the
   [shadPS4 patch collection](https://github.com/shadps4-emu/ps4_cheats/blob/main/PATCHES/Bloodborne.xml):

   ```sh
   mkdir -p runtime/downloads
   curl --fail --location \
     https://raw.githubusercontent.com/shadps4-emu/ps4_cheats/main/PATCHES/Bloodborne.xml \
     --output runtime/downloads/Bloodborne.xml
   ```

5. **Back up, then check.** Close shadPS4. Back up your saves. This check only
   looks at your files. It doesn't start the game or change anything:

   ```sh
   python3 play.py --check
   ```

6. **Play:**

   ```sh
   python3 play.py
   ```

   Or double-click `Play Bloodborne.command`. If you downloaded a ZIP, run
   `chmod +x "Play Bloodborne.command"` once first.

   The first time you visit an area, it may stutter while the emulator gets
   ready. That gets better the second time. Check the title screen, then
   controls, sound, and actual play. A passing check is only step one.

## Try the faster engine (bbport)

bbport skips most of the pretend-PS4 work and runs the game more directly.
It also listens to the keyboard on the menus (Space = Cross).

```sh
python3 play.py --engine bbport --install   # one time: download + safety check
python3 play.py --engine bbport             # play
python3 play.py --engine bbport --stats     # FPS summary of your last session
```

The first command downloads bbport's official release and checks its
fingerprint (SHA-256). If it doesn't match, it deletes the download and stops.
Everything goes in this repo's `runtime/` folder. Nothing goes in Applications.

The first time you play, the launcher does two things for you:

- It builds a game folder with update 1.09 already merged in. It uses Mac
  "clone" copies, so it takes almost no extra space. Your originals stay put.
- It **copies** your shadPS4 save over. Your shadPS4 save stays untouched.
  After that, bbport keeps its own save in `runtime/bbport/`.

The first launch can sit on a black screen for a few minutes while shaders
build. That's normal. bbport is newer and still has rough edges: a few effects
are missing on Mac, and things can pop in. Keep your shadPS4 setup as a backup.

### My crash fix for bbport

bbport 0.4-v1 sometimes stops mid-fight with `Unknown data_format=15`. The game
was still writing a vertex description when bbport read it. My patch swaps in a
plain stand-in format for that one draw, so the game keeps going. You can build it
with bbport's own scripts (the first run takes a while):

```sh
git clone https://github.com/bmy/bbport-mac ~/Documents/bbport-mac
cd ~/Documents/bbport-mac && git checkout 0.4-v1
git apply /path/to/this/repo/patches/bbport/vertex-format-standin.patch
bash tools/macos/setup_deps.sh && bash tools/macos/build.sh
cd /path/to/this/repo && python3 play.py --engine bbport --bbport-src ~/Documents/bbport-mac
```

Streaming or recording? Apply `patches/bbport/big-fps-counter.patch` too and add
`--fps-size 3` so viewers can read the FPS counter.

## Turn the knobs

Want to try other settings? Add these to the play command:

```sh
python3 play.py --help                     # list every option
python3 play.py --windowed                 # play in a window
python3 play.py --perf 4                   # turn off shadows for a few more frames
python3 play.py --resolution 1440p --fps 90 --perf 4
python3 play.py --extra "Disable AA" --check
python3 play.py --no-log
python3 play.py --keep-facegen
python3 play.py --keep-vulkan-validation   # debugging only; slower
```

I support 720p, 900p, 1080p, 1440p, and 4K, with 60, 90, or 120 FPS caps.
A cap is a speed limit, not a speed. **A 90 FPS cap does not create 90 FPS.**
Keep 720p and 900p as experiments; my baseline is 1080p.

The **perf level** turns off effects to save work. Higher numbers turn off more:

| Perf level | What it turns off |
| --- | --- |
| 0 | Nothing extra. Base speed patch, intro skip, FPS patch, and Facegen fix |
| 1 | Motion blur |
| 2 | Color fringing (chromatic aberration) |
| 3 — default | Some extra background renders |
| 4 | Dynamic light shadows |
| 5 | Soft corner shadows (SSAO) |
| 6 | Background blur (depth of field) |
| 7 | Glow (bloom) |

Each level includes the ones above it. `--keep-facegen` keeps the original
face code at any level. Repeat `--extra` to add named XML patches, and check
for conflicts.

The launcher turns Vulkan core validation off for play. It adds checks to many
graphics calls and can cost a lot of speed. Use `--keep-vulkan-validation` only
when I am chasing an emulator bug.

`--engine release` uses a separate install at
`runtime/Bloodborne Emulator.app/Contents/MacOS/shadps4`.
`--engine nightly-app` expects a separately prepared `Bloodborne Nightly.app`
at the same level. That game-category app bundle can turn on macOS Game Mode
in exclusive fullscreen. The launcher does not create it, and I have no
measured Game Mode speedup to share.

## Backups and the way home

Before the launcher changes your emulator settings, it saves a copy in
`runtime/config-backups/`. It writes its patches to
`~/Library/Application Support/shadPS4/patches/bloodborne-profile/` and keeps
session logs in `runtime/sessions/`. The profile also stays active in Qt Launcher.

To undo: close shadPS4, put back the settings copy you want, and put back your
old `bloodborne-profile` folder (or delete it if you had none).
**The launcher only backs up settings.** Back up your saves yourself.

I've seen first-visit stutter, graphics crashes, and the odd frozen loading
screen. Keep a working setup and change one thing at a time. Stuck? Try the
[troubleshooting prompt](docs/AGENT-INSTALL.md#help-the-hunt-broke) or my
[performance notes](PERFORMANCE.md).

## Credits and sharing

Thanks to [shadPS4](https://github.com/shadps4-emu/shadPS4),
[the patch authors](https://github.com/shadps4-emu/ps4_cheats),
[GoldHEN](https://github.com/GoldHEN/GoldHEN), and the homebrew developers whose
work made this possible. Bloodborne belongs to its rights holders.

My original code and docs use [the Unlicense](LICENSE). Fork away.
I do not include game data, firmware, keys, saves, or emulator bundles.
Please don't ask me for them. Want to help hunt frames?
[Here's how to contribute](CONTRIBUTING.md), including
[how I capture frame times](docs/FRAME-CAPTURE.md).
