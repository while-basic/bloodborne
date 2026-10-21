```text
Document:    My Bloodborne Windows and Linux Plan
Version:     v2.0.0
Author:      Christopher Celaya
Contact:     https://github.com/while-basic
Date:        2026-10-21
SHA256:      3fd23bcb5786239dbeb1f457f15a1ed5ce10eee880e13c4bea77382c4e520e38
Chain:       solana-mainnet
Tx:          4neYmX1QP9t2RZhoorHUEqw9PPZa6rtwtLD3pXcZEfUX2GhXKUYingnGzjcuihyQqnM7tMhPsvia1u3UQsmNqCYZ
License:     The Unlicense (public domain dedication)
```

# Bloodborne on a Windows or Linux PC

This is a plan, not a finished guide. This launcher's download, APFS copy,
and launch steps are Mac-only. I have not tested it on Windows or Linux.

The starting point is [upstream bbport](https://github.com/deadinside28/bloodborne_pc).
Check its current supported systems and build instructions before choosing
hardware or a setup route. A working Linux build does not prove a Windows
build works. You still need your own compatible game backup and update.

## The plan

1. Confirm the exact OS, CPU, graphics driver, game region, and update.
2. Follow bbport's own guide for a supported platform and get it running by hand.
3. Adapt this wrapper's install, copy, paths, and launch steps for that platform.
4. Preserve saves, provide a read-only check, and run local tests.
5. Check controls, sound, fullscreen, save/load, and a repeated crowd route.
6. Share only what I tested, with the hardware and build listed.

## Prompt you can paste

```text
Help me assess bbport on my Windows or Linux PC using
https://github.com/while-basic/bloodborne. Read README.md, AGENTS.md,
docs/WINDOWS-LINUX.md and the current upstream bbport guide first.

Ask about my OS, processor, graphics card, memory, free disk space, and my own
game backup and update. Check current platform support before installing.
This repo's launcher is Mac-only. Do not silently substitute another engine.

Explain one short step at a time. Preserve settings and saves. Ask before a
performance test. Keep setup checks, a launch, and real gameplay separate.
Do not download game files, firmware, or keys, upload my files, or use GitHub Actions.
```

## Checklist

- [ ] Supported bbport build boots my game on Linux.
- [ ] A supported Windows path is confirmed and tested.
- [ ] The wrapper's platform-specific steps are implemented and tested.
- [ ] Controllers, sound, fullscreen, save/load, and crowd play are checked.
- [ ] A plain-words guide is tried by someone who isn't me.
