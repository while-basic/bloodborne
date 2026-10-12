```text
Document:    Agent Installation Prompts
Version:     v1.1.0
Author:      Christopher Celaya
Contact:     https://github.com/while-basic
Date:        2026-10-12
SHA256:      084ea9c5650457ad5d332127e4793776ae231f0a5a3d90ecef1579eb4fc71f59
Chain:       solana-mainnet
Tx:          48fDDdaswWPkmhh8giiiNFDq5zdJAEwsz3Ld7ebXv3ZTLNp38EqM4KbGdqtdvSqTut1k35cDcBcJH5LsWQ8u3fVb
License:     The Unlicense (public domain dedication)
```

# Let your agent set it up

If you'd rather have your agent do the installation, copy the first prompt below.
It needs terminal access to your Mac. You'll still need to supply your own game
files and handle any steps that need your input.

I've included prompts for fixing an existing setup and checking performance too.
These are for the current Mac launcher and **CUSA00900 / 01.09**.
Windows, Linux, and the browser come later.

## Install it

```text
Set up https://github.com/while-basic/bloodborne on my Mac and help me launch
my own legally obtained copy of Bloodborne. Read the README and AGENTS.md
first, then do the setup.

Check my Mac, Python, and any existing shadPS4 install. Clone the repo if
needed, keeping my existing files and local changes. Install missing
Python 3.11+ and shadPS4 Qt Launcher from official sources or a trusted
package manager. Follow upstream Rosetta and emulator instructions without
bypassing OS security. If I'm not on macOS, tell me this wrapper isn't ready
for my platform.

Use Qt Launcher to install the pre-release engine. Open it once and close
it to create its config. Check the paths and config format against play.py;
don't guess if they differ.

Ask where my extracted CUSA00900 / 01.09 game folder is. Check its metadata,
or ask me to verify the region and version if you can't. If I only have a
disc, archive, PKG, or ISO, explain the upstream dump/import step I need.
Don't download game data, firmware, keys, updates, or DLC for me.

Check disk space, then copy the complete game folder to the path in the
README. Keep my original copy. Reuse an existing matching install rather
than overwriting it. Download Bloodborne.xml from the exact upstream URL
in the README. Record the emulator version and patch file hash.

Run the local tests and python3 play.py --check. Fix or explain any missing
prerequisites before going further. Back up my config, existing generated
patch profile, and saves before launch; tell me where the backups are.
The launcher's automatic backup covers config.json only.

If shadPS4 is running, ask me to close it normally. Launch with the default
1080p / 60 cap / perf 3 settings. Check the game window and gameplay, or
ask me to confirm them if you can't see them. A successful --check or a
running process isn't proof that the game works.

Tell me what you installed, what changed, and whether the game actually
ran. Keep game files, credentials, saves, and private logs local. Don't
push or upload anything, and don't use GitHub Actions.
```

## Fix my setup

```text
Help me fix my existing https://github.com/while-basic/bloodborne setup.
Read the repo instructions and check what I already have before changing
anything.

Check Python, shadPS4, the expected paths and config format, my complete
CUSA00900 / 01.09 game folder, and the Bloodborne.xml patches. Run the local
tests and python3 play.py --check. Use local logs to find the actual problem.

Back up settings, the generated patch profile, and saves before a repair.
Keep my original game files and other patch profiles. Don't start by
reinstalling everything or deleting caches and saves. If code needs to
change, use a separate branch/worktree.

Make the smallest fix that addresses the problem. Check it again and
launch after any running emulator has been closed normally. Verify the
game window or ask me to confirm what happens. Tell me what worked and
what still needs attention.

Don't download game data, publish changes, upload private logs, or use
GitHub Actions.
```

## Update it and check FPS

```text
Help me update and measure my https://github.com/while-basic/bloodborne
setup. Read the README and roadmap first. Keep my local changes and back
up settings, patches, and saves. Keep a way to return to my working emulator.

Record my computer specs, OS, drivers, power mode, display refresh rate,
game region/update, repo commit, emulator build/hash, patch XML hash,
resolution, FPS cap, and enabled patches. Update from official sources.

Use the same scene and route for several runs. Test first-visit shader
stutter separately from runs where shaders are already cached. Change one
setting at a time. Record average FPS, lows/frame times, stutter, crashes,
and any visual changes. Check controls, audio, game speed, and save/load too.

The README says Christopher is getting 24–55 FPS on an M5 Max with 128 GB
RAM. Measure what my machine does. A higher cap or a brief peak doesn't
prove sustained 90+ FPS. If you can't measure gameplay, give me the steps
to measure it and leave the results blank.

Keep game files, saves, and private logs local. Don't push changes, upload
anything, or use GitHub Actions.
```

If your agent gets stuck, have it tell you exactly what's missing.
Don't put your passwords, tokens, console keys, or game files in an issue.
