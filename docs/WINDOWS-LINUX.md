```text
Document:    My Bloodborne Windows and Linux Plan
Version:     v1.0.0
Author:      Christopher Celaya
Contact:     https://github.com/while-basic
Date:        2026-10-13
SHA256:      988b951d5812162b9ff1777ede87f58b13492260601383272e9662c2b7380722
Chain:       solana-mainnet
Tx:          5sNPqcUzkwTwfPfEGLUA4jXs4xRttJr6m7ryyy7J1H9osSQykPMvdEYtSMSrkvj1qUh9aoTiwGvpmP96ke9twfQL
License:     The Unlicense (public domain dedication)
```

# Bloodborne on a Windows or Linux PC

This is a plan, not a finished guide. I have not tested my launcher on Windows
or Linux yet. When I do, I'll check the boxes and share the numbers.

Good news first: a PC often has it easier than a Mac. shadPS4 runs natively on
Windows and Linux. No Rosetta in the middle. Most of the slow part on my Mac is
that extra translation step.

## What you need

- A PC with a modern 6-core or better processor. More speed per core helps most.
- A graphics card with current **Vulkan** drivers (most NVIDIA, AMD, and Intel cards
  from the last few years have them).
- Windows 10/11 or a current Linux, like Ubuntu or Fedora.
- Python 3.11 or newer.
- Your own **CUSA00900 / 01.09** game dump. Same rule as the Mac: bring your own.

The PS4 part of [the tutorial](PS4-TO-MAC.md) stays the same. Only the
computer side changes.

## The plan

1. **Get shadPS4 running by hand.** Use the official
   [shadPS4 downloads](https://github.com/shadps4-emu/shadPS4/releases) and
   [setup guide](https://shadps4.net/). Boot the game once with no launcher.
2. **Teach the launcher PC paths.** Today `play.py` looks in Mac folders.
   It needs the Windows and Linux places for shadPS4's settings, patches, and saves.
3. **Keep the same safety rules.** Back up settings first, change nothing during
   `--check`, keep saves out of experiments.
4. **Measure one crowd.** Same route I use on my Mac: Central Yharnam, the
   bonfire mob. Record FPS for a few minutes and keep the low numbers too.
5. **Check the boring stuff.** Controller, sound, fullscreen, save, and load.
6. **Write it up** in plain words, with the PC parts I tested.

Also worth a look: [bbport](https://github.com/deadinside28/bloodborne_pc), a
Bloodborne-only project. Its author reports high frame rates on Linux. It needs
the same kind of game dump. I haven't tested it.

## Prompt you can paste

Open Codex or Claude on your PC, in a folder you made for this, and paste:

```text
Help me set up Bloodborne on my Windows or Linux PC using
https://github.com/while-basic/bloodborne. Read README.md, AGENTS.md,
docs/WINDOWS-LINUX.md and docs/PS4-TO-MAC.md first.

Explain each step in plain words, one step at a time. I am not a programmer.
Before you run any command, tell me what it does.

Start by asking: my operating system, processor, graphics card, memory, free
disk space, and whether I already have my own CUSA00900 / 01.09 game dump.
Never download game files, firmware, or keys for me.

Get the official shadPS4 build for my system running first, without this
launcher. Then tell me what in play.py is Mac-only and what would need to
change for my system. Ask before changing any files or running a speed test.
Back up my settings and saves before the first launch.

Tell me separately: did the files check pass, did the game open, and did I
actually play. Keep my files private. Do not upload, push, or use GitHub Actions.
```

## Checklist

- [ ] shadPS4 boots my game on Windows by hand.
- [ ] shadPS4 boots my game on Linux by hand.
- [ ] `play.py` finds the right folders on both.
- [ ] Crowd FPS measured on one PC, with the parts listed.
- [ ] Controller, sound, fullscreen, save, and load checked.
- [ ] Plain-words guide written and tested by someone who isn't me.
