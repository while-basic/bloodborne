```text
Document:    My Bloodborne Agent Guide
Version:     v3.0.1
Author:      Christopher Celaya
Contact:     https://github.com/while-basic
Date:        2026-10-21
SHA256:      728a099eac2906911a79d317d95d0cba6453cb244e7a7fb8bcb06482ede80eff
Chain:       solana-mainnet
Tx:          2UUnMx7GsGCy1DSVDu3d2KoM6ygbHXmbw1ieZsca2jqTUCtEU5SSNf1nJzPcJrQDi14Rs9L2NPsPHSh8wqCDFcrw
License:     The Unlicense (public domain dedication)
```

# Help me keep the hunt honest

I'm Christopher Celaya, [while-basic](https://github.com/while-basic).
This repo launches **bbport for Mac only**. Read README.md, the walkthrough,
CONTRIBUTING.md, and PERFORMANCE.md before changing the setup.

## Voice and public sharing

- Write as “I” and “my,” and speak to readers as “you.” Use short, everyday
  words. A little fun fits; fake FPS does not.
- My earlier 50+ FPS footage reached more than a million people. That is my
  report about the footage, not a fresh benchmark or a bbport guarantee.
- Original code and docs use the Unlicense. Keep upstream license text and
  credit intact. The bbport patches keep their GPL-2.0-or-later license.
- Document headers use my name, GitHub contact, and the Unlicense. Seal changed
  headed files on both chains before commits. If anchoring fails, stamp and
  record why. In private upstream clones I never push, stamp only.
- Keep games, updates, firmware, keys, saves, edited game assets, engine bundles,
  credentials, local agent config, and raw logs out of Git. Audit staged files
  and history before publishing. Never run GitHub Actions.

## Setup and preservation

- Use an isolated Git worktree for code. Run CONTRIBUTING.md checks locally.
  Commit finished changes; merge and push only with direct authorization.
  Keep one short completion note here after a commit.
- Do not add standalone-engine launch paths or change another app's settings.
  The hidden `--engine bbport` flag only keeps old bbport commands working.
- Keep 1080p / 60 cap / perf 3 as the default. Preserve the existing bbport
  game, settings, saves, and other worktrees. Never overwrite a good save.
- My external SSD is off-limits: do not inspect, mount, read, or write it.
- Before console setup, ask about exact firmware, game region/update, Mac specs,
  USB/Ethernet gear, backups, free space, and protected drives. Check current
  primary sources. Do not update firmware, reset a console, format drives,
  or change unrelated networks as a shortcut.
- Identify a queued system update before helping remove it. Leave game updates
  and saves alone. Loader, transfer, install, launch, and actual play are
  separate checks. Ask what the console shows when you cannot see it.

## Testing and evidence

- Ask before a system performance/load test; describe its duration and load.
  Honor permission already given in this session. No benchmark is requested
  by the bbport-only publishing task.
- Use copied saves and a separate test folder for experiments. Check controls,
  sound, game speed, visuals, save/load, stutter, and crashes as well as FPS.
- Compare the same scene and warm-cache route. A cap, menu FPS, running process,
  or draw-count filter does not prove real gameplay performance.
- Heavy tracing and debugger attachment remain off during ordinary play tests.
  Older private profiling state remains in ignored runtime/optimization-state.json;
  do not restart those paused experiments without a new instruction.

## Current handoff

The private CSR copy and desktop shortcut use bbport and separate copied saves
under `runtime/mods/csr/`. The text/archive and font-preview checks passed;
in-game appearance and PS4 installation remain unverified. Do not include those
edited game files in a release. The normal launcher does not apply the mod.

The optional vertex-format stand-in and bigger FPS counter patches build, but
long play with the stand-in is still unverified. See PERFORMANCE.md for measured
bbport results and their limits; 90+ FPS gameplay is still a goal.

## Completion note

2026-10-21: I made the launcher and public guides bbport-only, removed the old
standalone tools, and kept the CSR sources. All 19 tests, the name self-check,
installed-file check, and secret scans pass; no new gameplay benchmark was run.

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
