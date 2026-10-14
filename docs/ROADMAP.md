```text
Document:    My Bloodborne Roadmap
Version:     v2.2.0
Author:      Christopher Celaya
Contact:     https://github.com/while-basic
Date:        2026-10-13
SHA256:      6fe76f9b6bc0606fecf840f674997f25046d91d9b6d6627fc0db5016cbc75202
Chain:       solana-mainnet
Tx:          5Cwr9agdk6PYJwj9tdKKiGMhQEHSoqnCeVNbbiFBRCfK3CM3eJk7F9EKVK592N2bEeyBsAnYUBMsFbQZaviW8QaE
License:     The Unlicense (public domain dedication)
```

# One hunt at a time

I got my own Bloodborne copy running on my M5 Max. More than a million people
have seen the 50+ FPS footage. Now I want to make it run better, then help more
people play their own copy on more computers.

## Done: disc to Mac

- [x] Load homebrew on my PS4 11.02 with a matching browser loader and payload.
- [x] Set up the USB-C Ethernet link and local file transfers.
- [x] Back up my disc and matching update, then launch CUSA00900 / 01.09 on Mac.
- [x] Add resolution, FPS, and performance patch choices.
- [x] Add config backups, a read-only setup check, and private logs.
- [x] Enable pipeline caching and async logs; disable Facegen by default.
- [x] Add a light recorder for CPU and whole-machine GPU activity.
- [x] Share a guide that asks about gear, firmware, backups, and test permission.
- [x] Add Codex and Claude prompts, plus USB and Ethernet paths.

These checks cover my setup and the tools in this repo. I have not personally
tested every firmware route linked in the [tutorial](PS4-TO-MAC.md).

## Next: 60+ FPS in crowds, then 90+

My crowd test is the bonfire mob in Central Yharnam. There my Mac holds about
40–48 FPS. Settings alone don't fix it: the slow part is the Mac's processor
translating PS4 game code. So I'm also testing
[bbport for Mac](https://github.com/bmy/bbport-mac), a Bloodborne-only project.

- [x] Fix the test scene and route (Central Yharnam crowd).
- [x] Add bbport as a launcher engine (56–59 FPS where shadPS4 gave 43–48).
- [ ] Hold 60+ FPS through the crowd fight, measured, not guessed.
- [ ] Record the engine build, patch hashes, power mode, and display refresh.
- [ ] Capture real FPS and frame times across repeated warm-cache runs.
- [ ] Find the slow work in game execution, graphics, or frame pacing.
- [ ] Test one change at a time and keep a way to return to the baseline.
- [ ] Check picture quality, game speed, controls, sound, crashes, and saves.
- [ ] Reach and repeat 90+ FPS during play at a stated resolution and quality.

My baseline is 1080p / 60 cap / perf 3. I keep lower-resolution experiments
separate. Choosing a 90 FPS patch does not check the last box. A short peak or
an empty scene does not check it either. See [my notes](../PERFORMANCE.md).

## Then: Windows and Linux

- [ ] Replace Mac-only paths and launch steps.
- [ ] Test each platform's Vulkan drivers and emulator build.
- [ ] Check controllers, sound, fullscreen, and save/load.
- [ ] Publish tested hardware and clear setup steps.

The full plan and a paste-in prompt live in [WINDOWS-LINUX.md](WINDOWS-LINUX.md).

shadPS4 already supports more than Mac. This small wrapper still needs its own
work and tests on those systems.

## Later: the browser

- [ ] Choose between local browser execution and streaming from a host computer.
- [ ] Build a small proof of the chosen path.
- [ ] Measure input delay, picture quality, storage needs, and performance.

There is no browser build yet. This box gets a lot bigger when you open it.

## What counts as a result

I share the machine, OS, engine and repo commits, game version, patch hash,
resolution, FPS cap, vblank, power mode, and display refresh. I keep first-visit
shader stutter separate from cached runs and include slow frames and crashes.
Raw traces, game files, and saves stay local. More frames are only a win if the
game still works.
