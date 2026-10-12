```text
Document:    Bloodborne Launcher Agent Instructions
Version:     v1.3.0
Author:      Christopher Celaya
Contact:     https://github.com/while-basic
Date:        2026-10-12
SHA256:      fd989ac7722f338a313c620b6e5d3797374dd990fac676270113b5d0ae6c27e8
Chain:       solana-mainnet
Tx:          5izqrnBGqwj2ewPr45mgoQswH2767fVupdm7yiHZ4jGGYXXXECqCCY6rUB9viyFN2NcfqQUnLFuEbgzMjcjp6QPP
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

## Decisions still open
The existing repository is while-basic/bloodborne and is public. The current session authorizes pushing the reviewed work to main; no new repository is needed. Still confirm the target resolution/quality for 90+ FPS and whether browser work means local execution or streaming. Keep older route FPS measurements separate from the latest qualitative boss-test report.

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

2026-10-12: `61e99d5` records the working 1080p profile, the rejected 900p trial, and the next-session guide; launcher help now qualifies earlier FPS and bottleneck claims. Local checks pass and private runtime data stays untracked.

## Runtime profiling and next session
2026-10-12: The restored 1080p / 60 FPS target / perf 3 run was reported as “very good.” Use the nightly binary, borderless fullscreen, requested Mailbox (driver falls back to Fifo), vblank 60, and FPS text scale 2.5. The exact command is in PERFORMANCE.md. No measured FPS was supplied for this run.
The 900p boss attempt was reported as extremely laggy; its resolution patch is removed. Preserve the working 1080p baseline. Only the FPS text size differs from the earlier setup; saves were not restored.
Use profile_runtime.py with --seconds 3600 --interval 2 during play; renew before its limit if needed, wait for the user's death report, then stop only the recorder with SIGINT. It cannot see the scene, detect death, or measure FPS. Keep heavy Metal/Instruments tracing off during combat; it previously added major overhead.
Raw recordings, logs, settings, and saves stay private under ignored runtime/. The 1080p and 900p attempts end in 172604681876Z and 173400966672Z; the latter has the comparison and rollback record. PERFORMANCE.md has the resume instructions and local evidence pointers. Native ARM game entry remains unimplemented.

<!-- graft:start -->
## Graft — repo context graph

This repo is indexed in `graft/`: small linked markdown nodes that explain each
system and carry exact file:line spans, kept in sync with the code through git.

For ANY task here — understanding how something works, finding where code lives,
or scoping a change — get context from the graph before grepping or opening
source files. Re-ask freely (it's cheap) and reuse literal identifiers you
already have (symbol, error string, file name) as the query. New to this repo?
Run `graft map` first — a token-budgeted orientation (dir clusters, hubs,
hotspots), no LLM, no key.

- Run `graft ask "<your question>" --source` → ranked nodes with the relevant
  code spans inlined (each hit's ≤8-line crux by default; `--full` for whole
  definitions when the crux isn't enough). Match the tool to the task shape:
  for understanding or editing, the top node IS the answer — cite its
  `covers:` file:line spans and edit straight from `--source`. For
  exhaustive tasks ("every occurrence / every caller of this pattern"), ranked
  results are top-N, not complete — run `graft grep "<literal>"` instead
  (exhaustive over indexed files, grouped by enclosing symbol), falling back
  to raw `grep -rn` only for unindexed files.
- `graft skeleton <file>` → every definition's signature + span, ~10× cheaper
  than reading the file; use it to skim an API surface.
- `graft callers <symbol>` gives precomputed, exact edges — who calls this.
  Add `--direction out` for what it calls, or `--depth N` to walk
  transitively for the full blast radius. For structural questions, skip
  ranking and use this directly.
- Or browse: `graft/INDEX.md` lists every node; follow the links.
- Monorepos and folders of multiple repos rank fairly across sub-projects —
  hits carry `[scope/]` labels naming which one they're from. Narrow with
  `graft ask "<task>" --in <scope>/` once you know where you're working.

If a returned span is truncated ("+N more lines"), open the file at that exact
range before finalizing. Only open source files when a node genuinely lacks a
needed detail, and then at the exact file:line the node points to — never
re-read whole files.

After big code changes, refresh the graph with `graft build` (deterministic,
no API key, $0).
<!-- graft:end -->
