```text
Document:    My Codex and Claude Setup Prompts
Version:     v3.0.0
Author:      Christopher Celaya
Contact:     https://github.com/while-basic
Date:        2026-10-21
SHA256:      a74bbe8426dd802a626bf5ee07a528905c5337a0ea63dbbb3d3cb8dd30f0cd6d
Chain:       solana-mainnet
Tx:          4otYovXo29X1mqw3pgMsYqbFLq58EPXYPbHyqQFyLy5VX5EnTAJmHvCoeTnDLmzWQuvvR2rJubw7HzMC2CbCSUAT
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
Check specs and current bbport for Mac requirements first; if I approve a load test,
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
explain what it can and cannot tell me. Use the pinned bbport for Mac guide.

Use Python 3.11+ and bbport for Mac only. Run python3 play.py --install to
fetch the pinned official release and check its SHA-256. Follow the upstream
Rosetta instructions. Do not bypass macOS security prompts or substitute
another engine.

Verify CUSA00900 / 01.09 from game metadata. A renamed folder is not proof.
Keep the original backup. Put a full merged game in runtime/games/CUSA00900-109,
or use the separate base/update layout in the README. Do not fetch game data,
keys, or firmware. No separate community patch download is needed.

Run the local checks in CONTRIBUTING.md and python3 play.py --check.
Back up runtime/bbport before launch if it exists. That folder holds this
launcher's settings and saves. Do not overwrite an existing save or import
one without my instruction. The launcher does not import saves automatically.

After any running game closes normally, launch at 1080p / 60 cap / perf 3.
The first launch can sit on a black screen while shaders build. Verify the
game window, controls, sound, and actual play. Ask me to confirm what you
cannot observe. Keep file checks and gameplay separate. After quitting,
python3 play.py --stats summarizes the latest frame CSV.
Keep private files local. Do not push, upload, or use GitHub Actions.
```

## Help, the hunt broke

```text
Help repair my existing Bloodborne launcher setup. Read the repo instructions.
Inspect my current install, local changes, and logs before changing anything.
Check the bbport build, game version, runtime/bbport settings, and --check output.

Back up runtime/bbport settings and saves. Keep the original
game and working bbport build. Do not start by deleting caches or reinstalling
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

Keep a working bbport build and backups of settings and saves. Record
hardware, OS, display refresh, power mode, game version, repo and bbport
commits, engine/patch hashes, resolution, FPS cap, and enabled patches.

Use the same scene, camera, route, and warm shader cache. Change one thing
at a time. Repeat runs and record FPS/frame times, stutter, crashes, and visual
changes. Check game speed, controls, sound, and save/load. Separate menus,
loading, deaths, and first-visit shader work from the gameplay comparison.

Do not run heavy Metal/Instruments tracing during combat. Do not infer
FPS from CPU use. A higher cap, static scene, or short peak cannot prove steady
90+ FPS. Keep unmeasured results blank and roll back failed experiments.

Run python3 play.py --stats after each session. The draw-count filter does
not recognize a scene; use the route you actually observed.
Keep raw evidence local. Do not upload, push, or use GitHub Actions.
```
