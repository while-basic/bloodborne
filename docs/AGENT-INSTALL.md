```text
Document:    Bloodborne — Agent Installation Prompts
Version:     v1.0.0
Author:      Christopher Celaya
Contact:     https://github.com/while-basic
Date:        2026-10-12
SHA256:      d9996f36440c5ff25f5c5ec2f09a75e46999bc4b983bd85d1cdf81e8a332f97f
Chain:       solana-mainnet
Tx:          gJCx25qLyjDPNpA1ex23J8Ajdki1hzwo3ETCh9XzXbZ7p3neS7TbBpcvboeSUa65QtSS1kGtamvthXYA2CMViEM
License:     The Unlicense (public domain dedication)
```

# Have your agent install Bloodborne on Mac

Copy a prompt below into an agent with terminal access to your Mac, such as
Codex, Claude Code, or another coding assistant. The agent can prepare the
launcher and dependencies; you supply your own legally usable game files.

This is Christopher Celaya's open-source project:
**https://github.com/while-basic/bloodborne**.

The current wrapper is for **macOS**, with a tested **CUSA00900 / 01.09** game
profile. Windows, Linux, and browser support are future work. The tested machine
is an M5 Max with 128 GB memory; that is not a minimum requirement or FPS guarantee.

## 1. Install and launch

Copy this entire block. Your agent should ask for your game folder if it
cannot identify it safely.

```text
Install https://github.com/while-basic/bloodborne on this Mac and help me run
my own legally obtained Bloodborne files. Read README.md, AGENTS.md, and
docs/AGENT-INSTALL.md first. Work through the setup, not just a list of advice.

1. Inspect my OS, CPU/GPU, memory, Python, and existing shadPS4 installation.
   This wrapper currently supports macOS only. If I am on Windows or Linux,
   report that limitation and stop before installing the Mac wrapper.
2. Clone the repo into an appropriate project folder if it is not already
   present. Preserve existing files and local changes. Do not overwrite an
   unrelated folder or reset an existing checkout.
3. Install missing Python 3.11+ and shadPS4 Qt Launcher only from their
   official sources or a trusted package manager. Reuse compatible existing
   installs. Follow upstream macOS/Rosetta and emulator setup instructions;
   do not bypass operating-system security protections.
4. Use Qt Launcher to install the pre-release engine. Open it once to create
   its configuration, then close it. Confirm that the exact engine and config
   paths expected by play.py exist. If current upstream paths or the config
   schema differ, explain the mismatch instead of guessing or writing over
   settings. Identify missing console files from upstream documentation;
   ask me to supply them.
5. Ask me where my extracted Bloodborne CUSA00900 version 01.09 files are.
   Check the title ID and version from available game metadata. If the
   metadata cannot confirm them, ask me to verify them before applying patches.
   Do not download game files, firmware, keys, updates, or DLC. A physical
   disc, PKG, ISO, or ZIP alone is not the extracted game directory required
   here; explain the upstream import/dumping step if that is what I have.
6. Check free space before copying the complete game folder to
   runtime/games/CUSA00900/. Do not move or delete my original copy.
   If the target already contains a game, verify it and reuse it; do not
   overwrite it. Obtain Bloodborne.xml from the exact official patch URL
   in README.md and store it in runtime/downloads/. Keep third-party
   license notices and record the emulator version and patch file hash.
7. Run the local tests and python3 play.py --check. Review the check output:
   it validates local prerequisites and patch selection, not gameplay.
   Stop and explain missing prerequisites or incompatible patches.
8. Before launch, make a separate backup of my current shadPS4 config,
   existing bloodborne-profile patch folder if present, and saves using
   upstream guidance. Tell me where the backups are. The launcher's own
   automatic backup covers config.json only.
9. If shadPS4 is running, ask me to close it; do not force-kill it. Start
   python3 play.py at its default 1080p / 60 cap / perf 3 settings. Check
   the visible game window, not just the process exit status. If you cannot
   inspect it, ask me to confirm the title screen and actual gameplay.
10. Summarize what you installed, what changed, where backups are, and
    whether real gameplay was observed. The maintainer reports 24–55 FPS;
    90+ FPS is a future goal, not a result you should promise.

Keep game data, saves, firmware, keys, credentials, and private logs out of
Git and uploads. Do not publish or push anything. Do not use GitHub Actions.
```

## 2. Check or repair an existing setup

```text
Diagnose my existing https://github.com/while-basic/bloodborne setup on
macOS. Read the repo instructions and inspect the actual checkout before
changing anything. Do not reinstall everything or download game data.

Check Python, the shadPS4 engine and config paths, the complete local game
folder, CUSA00900 / 01.09 compatibility, and the upstream Bloodborne.xml
patch names/version. Run local tests and python3 play.py --check. Review
recent local logs without uploading them or exposing private information.

Identify the specific failure. Back up config, the existing generated patch
profile, and saves before any repair. Preserve other patch profiles and my
original game files. Do not delete shader caches or saves as a first step.
If an upstream update changed the config schema or paths, explain the exact
difference and make any needed code repair on a separate branch/worktree.

Apply the smallest supported fix, re-run the check, and launch only after
any running emulator has been closed normally. Verify the visible result
or ask me to confirm it. Report actual results and remaining blockers.
Do not claim gameplay is verified from --check alone. Do not push changes,
upload logs, or use GitHub Actions.
```

## 3. Update and measure performance

```text
Help me update and benchmark my https://github.com/while-basic/bloodborne
setup on macOS. Read README.md and docs/ROADMAP.md. Preserve local changes,
game files, saves, and my current working emulator. Back up settings and
patch profiles before changing them.

Record the current commit, emulator build/hash, patch XML hash, game
region/update, Mac specs, macOS build, power mode, display refresh rate,
resolution, FPS cap, and enabled patches. Update only from official upstream
sources, with a way to return to my previous working setup.

Compare the same scene and route over several runs. Separate first-run
shader stutter from warm-cache results. Change one setting at a time.
Report average FPS, lows/frame times, visual differences, crashes, and
whether controls, audio, game timing, and save/load still work.

The current owner-reported range is 24–55 FPS on an M5 Max with 128 GB RAM.
90+ FPS is a development goal. A 90/120 FPS cap, an overlay peak, or a
successful launch is not proof of sustained 90+ FPS. If you cannot measure
the game directly, give me a short measurement procedure and leave results
unverified. Do not invent measurements or upload private logs/game files.
Do not push changes or use GitHub Actions.
```

## If your agent needs your help

A console dump, a missing update, an OS permission prompt, or a visible gameplay
check may need your input. The agent should name that exact step and continue
with any independent setup it can safely complete. Never paste account passwords,
tokens, console keys, or game data into a public issue.
