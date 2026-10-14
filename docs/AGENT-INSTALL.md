```text
Document:    My Codex and Claude Setup Prompts
Version:     v2.1.0
Author:      Christopher Celaya
Contact:     https://github.com/while-basic
Date:        2026-10-14
SHA256:      252a08fe7812c4c3e5a160873714c39aa2be6f17318d4ca2a4bc9200edcd1437
Chain:       solana-mainnet
Tx:          4LafLqwzmpsNWCD5VpNfAAXcf9djXf1jncY74X1JNegwFDGd8hyXfRVAdXWyH7rs7QYfkE4D3EtSfaTnCjGePmfX
License:     The Unlicense (public domain dedication)
```

# Bring an agent to the hunt

I used Codex and Claude to help with Mac commands and PS4 steps. Pick either
agent with local terminal access, open this repo, and paste a prompt below.
You still handle the console, cables, and any checks the agent cannot see.
Keep passwords, console keys, saves, and game files out of chat and issues.

## Start with my disc and PS4

```text
Help me go from my own Bloodborne disc or digital copy to playing on my Mac
using https://github.com/while-basic/bloodborne. Read README.md, AGENTS.md,
CLAUDE.md, and docs/PS4-TO-MAC.md. Walk me through one short step at a time.
Ask what each screen shows before moving past a console step you cannot see.

Start by asking what I have: exact PS4 firmware, Mac chip/RAM/macOS, disc or
digital copy and game region/update, controller, free internal space, backups,
USB drive, Ethernet cable, USB-C Ethernet adapter, and any existing homebrew.
Ask which drives must stay untouched. Never assume a USB drive is empty.

Ask permission before a Mac performance test. Explain the duration and load.
Check specs and current shadPS4 requirements first; if I approve a load test,
use a short local test. A synthetic result cannot guarantee game performance.
Do not upload hardware reports. Let me skip testing and continue the guide.

Before putting the PS4 online, help me check Notifications / Downloads for a
queued SYSTEM SOFTWARE update. Identify it and explain its removal before I
delete it. Leave game updates, games, and saves alone. Help me turn off auto
system downloads. Do not update, downgrade, reset, or initialize my console.

Verify my exact firmware against current primary project guides. Link the
chosen method, supported firmware and payload, required gear, and recovery
steps. Do not assume all 13.xx versions work or confuse a browser vulnerability
with a complete jailbreak. Ethernet on 11.02 does not mean PPPwn supports it.
Avoid any route that needs a full-system restore or drive erase by default.

Choose USB or Ethernet for each job based on my gear. Explain the difference
between loading the jailbreak, installing a homebrew PKG, and dumping a game.
For direct Ethernet, identify the actual adapter and record existing network
settings. Use a free local subnet and guide me through both ends. Do not guess
interface names, enable Internet Sharing, or change unrelated network services.

Confirm GoldHEN on the console before installing homebrew from its maintainer.
Verify the homebrew app opens; a transferred PKG is not an installed app.
Follow the current upstream guide to dump my own base game, matching 01.09
update, and required modules. Copy to an approved folder and verify the copy.
A plain FTP copy of encrypted installed files may not be a usable dump.

Then follow the Mac setup prompt below. Keep my original data and a rollback
path. Do not download games, publish my files, or use GitHub Actions.
```

## I already have my extracted game

```text
Set up https://github.com/while-basic/bloodborne on my Mac. Read its README,
AGENTS.md, and CLAUDE.md first. Check what is installed and preserve my work.

Ask for my Mac specs, game folder, game region/update, available space, and
drives to avoid. Ask permission before running a performance/load test and
explain what it can and cannot tell me. Use official shadPS4 requirements.

Use Python 3.11+, shadPS4 Qt Launcher, and the upstream Rosetta setup. Install
the pre-release engine, then open and close it to create its config. Check
paths and config format against play.py. Don't bypass macOS security prompts.

Verify CUSA00900 / 01.09 from game metadata. A renamed folder is not proof.
If I have a disc, PKG, or archive, walk me through the upstream dump/import
step first. Reuse a matching complete install; keep the original backup.
Get Bloodborne.xml from the exact upstream URL in the README. Record the
emulator build and patch hash. Do not fetch game data, keys, or firmware.

Run the local checks in CONTRIBUTING.md and python3 play.py --check.
Back up config, the existing generated patch profile, and saves before launch.
Tell me where each backup is. The launcher's backup covers config only.

After any running emulator closes normally, launch at 1080p / 60 cap / perf 3.
Verify the game window, then controls, sound, and actual gameplay. Ask me to
confirm what you cannot observe. Report setup checks and gameplay separately.

Once shadPS4 works, offer the faster bbport engine from the README. Run
python3 play.py --engine bbport --install (it checks the download's SHA-256),
then launch with --engine bbport. It copies my shadPS4 save once; keep the
shadPS4 setup as a backup. A black screen during the first shader build is
normal. Afterward, python3 play.py --engine bbport --stats sums up FPS.
Keep private files local. Do not push, upload, or use GitHub Actions.
```

## Help, the hunt broke

```text
Help repair my existing Bloodborne launcher setup. Read the repo instructions.
Inspect my current install, local changes, and logs before changing anything.
Check the emulator, game version, config format, patch file, and --check output.

Back up settings, the generated patch profile, and saves. Keep the original
game and working emulator. Do not start by deleting caches or reinstalling
everything. Use a separate worktree if code changes are needed.

Fix the cause, run the local checks, and verify a real launch. Ask me what I
see if you cannot view gameplay. Keep the report short and name any blocker.
Do not download games, upload logs, publish changes, or use GitHub Actions.
```

## Help me hunt frames

```text
Help measure and improve my Bloodborne setup. Read PERFORMANCE.md and the
roadmap. Ask permission for performance tests and agree on the resolution,
picture quality, test length, and scene before changing settings.

Keep a working emulator and backups of config, patches, and saves. Record
hardware, OS, display refresh, power mode, game version, engine (shadPS4 or
bbport), repo and engine commits, engine/patch hashes, resolution, FPS cap, vblank, and enabled patches.

Use the same scene, camera, route, and warm shader cache. Change one thing
at a time. Repeat runs and record FPS/frame times, stutter, crashes, and visual
changes. Check game speed, controls, sound, and save/load. Separate menus,
loading, deaths, and first-visit shader work from the gameplay comparison.

profile_runtime.py reads CPU/GPU activity; it does not measure FPS or see the
scene. Do not run heavy Metal/Instruments tracing during combat. Don't infer
FPS from CPU use. A higher cap, static scene, or short peak cannot prove steady
90+ FPS. Keep unmeasured results blank and roll back failed experiments.

For bbport, run python3 play.py --engine bbport --stats after each session.
Keep raw evidence local. Do not upload, push, or use GitHub Actions.
```
