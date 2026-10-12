```text
Document:    Bloodborne Launcher Agent Instructions
Version:     v1.2.0
Author:      Christopher Celaya
Contact:     https://github.com/while-basic
Date:        2026-10-12
SHA256:      baec931ccd3a0c7e2eae01e2cc0b8639f5a9aaf62fb7dedc66dc8900c3902833
Chain:       solana-devnet
Tx:          Y4w3CxWxhQKSap1u9rRJHL95fXHXV1jvbkSeSs1J4166UaBiXBgaNkVLQ7hH6K2MRJEkWsvvBpPVvbyayAwv6aH
License:     The Unlicense (public domain dedication)
```

# Agent instructions

- Use graft first for code context. If the source checkout has no index, build
  the local, ignored index or use the global session hook.
- Work in an isolated worktree and commit finished changes. Do not merge into
  main or publish without the user's direct instruction.
- Never use GitHub Actions. Run the local checks in CONTRIBUTING.md.
- Do not commit game data, firmware, keys, saves, emulator bundles, private logs,
  or local agent configuration. Review history as well as the current tree.
- Keep the current 24–55 FPS report separate from FPS cap settings. A dry run
  cannot verify gameplay. The roadmap order is Mac 90+ FPS, Windows/Linux, browser.
- This is Christopher Celaya's personal project: https://github.com/while-basic.
  Write public pages in Christopher's direct, first-person voice. Avoid reports
  about "the owner," corporate release language, and repeated disclaimers.
  Original code and docs use the Unlicense; retain third-party credits and rights.
  Keep the upstream standard LICENSE text unchanged for license detection;
  its document metadata lives in docs/LICENSE-NOTES.md.
- Produced documents use the standard header fields with Christopher Celaya as
  author, the personal GitHub URL as contact, and the Unlicense. Anchor
  changed header-bearing files with docseal on both chains before committing;
  if anchoring fails, stamp and document the reason.
- After each commit, add or refresh one short completion note here.

## Public release decisions still open

The owner authorized public publication and profile pinning under while-basic.
Confirm the exact emulator revision, settings and route for the
24–55 FPS report, target resolution/quality for 90+ FPS, and whether browser work
means local execution or streaming. The system specs were read from the local
Mac; confirm it is the same machine used for the reported range.

The separate m5-emulation worktree has uncommitted experimental launcher changes.
Do not include them in this release without review. No full gameplay benchmark
was run while preparing these public docs.

## Completion note

2026-10-12: Rewrote the public README, roadmap, contribution guide, and agent
prompts in Christopher's first-person voice, retaining setup details and limits.
The personal repo is public and pinned, with GitHub-recognized Unlicense terms.
Two dry-run tests pass; real local prerequisites pass without launching or writing
config. History/file screening and ignore checks pass. Gameplay was not retested.

Document sealing: the earlier launcher mainnet timeout was resolved on retry
during the personal rebrand. Headers record the latest successful anchors.
The license-notes mainnet submission failed simulation; its devnet anchor and
local hash stamp succeeded, and its header records that available evidence.

2026-10-12 (later): Merged the m5-emulation launcher work into main after live-play
measurements: `--engine nightly-app` (game-category bundle, the only way macOS Game Mode
engages, exclusive fullscreen only), `--fullscreen-mode`, `--present-mode`, `--vblank`,
720p/900p test sizes, Facegen disabled by default (`--keep-facegen`). README carries the
measured table and the CPU-bound conclusion (crowd floor ~41 FPS at 1080p). Local checks
pass (2 tests, py_compile, --help, diff --check). Gameplay was measured by hand with the
DualShock, not by a scripted route.
