```text
Document:    Bloodborne Launcher Agent Instructions
Version:     v1.0.0
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-10-12
SHA256:      2abe9dc30ad6c011ebbe94db9a9b53bf6f5d1e032a1b6b8e888a26a1c0ae8f32
Chain:       solana-mainnet
Tx:          5kEpaXxMdEzSpdKFsNSkWffafi27kMVz6eweV57kMgg2mJR3hW2BcdkF2ZSpzzFu6GZAhoe3SE5C7cg9z2BVmfY8
License:     All Rights Reserved / Celaya Solutions
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
- Preserve the current All Rights Reserved notice until the owner selects a license.
- All produced documents need the standard Celaya Solutions header. Anchor
  changed header-bearing files with docseal on both chains before committing;
  if anchoring fails, stamp and document the reason.
- After each commit, add or refresh one short completion note here.

## Public release decisions still open

Confirm the GitHub owner/name and permission to publish; no remote is configured.
Confirm the source license, exact emulator revision, settings and route for the
24–55 FPS report, target resolution/quality for 90+ FPS, and whether browser work
means local execution or streaming. The system specs were read from the local
Mac; confirm it is the same machine used for the reported range.

The separate m5-emulation worktree has uncommitted experimental launcher changes.
Do not include them in this release without review. No full gameplay benchmark
was run while preparing these public docs.

## Completion note

2026-10-12: Public-release preparation adds setup, system specs, roadmap, contribution
notes, file exclusions, and an honest dry-run result; publication remains pending.
Prepared on the codex/public-release branch; main and the experimental worktree
remain unchanged, and no GitHub repository has been created or published.
Two dry-run tests pass; real local prerequisites pass without launching or writing
config. History/file screening and ignore checks pass. Gameplay was not retested.

Document sealing: the launcher mainnet transaction did not confirm within docseal's
60-second window; it may still land. Its devnet anchor succeeded, so the launcher
header currently records devnet. Local hashes were stamped as the required fallback.
