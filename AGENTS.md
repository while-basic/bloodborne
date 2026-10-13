```text
Document:    My Bloodborne Agent Guide
Version:     v2.7.0
Author:      Christopher Celaya
Contact:     https://github.com/while-basic
Date:        2026-10-13
SHA256:      275b5dd2db26adf4dc7ceb9fbbedcb9d429a3a947b57ccd22e43058bd3cd75e8
Chain:       solana-mainnet
Tx:          3YsQmfFgnS9Jmw7sWmHEfzdVHtnDpyR9Qd3XWWsPRujStTyEYV8iNNprp57iicmLsfd2vojoTWA323tM66nkQXCp
License:     The Unlicense (public domain dedication)
```

# Help me keep the hunt honest

I'm Christopher Celaya, [while-basic](https://github.com/while-basic). This is
my personal Bloodborne launcher. Read the README, tutorial, contribution
checks, and performance notes before changing the setup.

## Voice and public docs

- Write about my work as “I” and “my.” Speak to readers as “you.” Do not call
  me “the user” or “the owner” in public docs.
- Use short sentences and everyday words. A little fun fits; fake FPS does not.
- My shared footage shows 50+ FPS and has reached over a million viewers.
  That is my report, not a repeatable benchmark. Keep historical measurements,
  later play reports, FPS caps, and new tests separate.
- Original code and docs use the Unlicense. Keep upstream LICENSE text intact;
  its document header belongs in docs/LICENSE-NOTES.md. Keep third-party credit.
- New documents use the standard header fields, my name, my GitHub contact,
  and the Unlicense. Seal changed header-bearing files with docseal on both
  chains before commits. If it fails, stamp locally and record the reason.
  In private upstream clones that I do not push, stamp only.

## Setup help

- Ask about exact firmware, Mac specs, game region/update, USB, Ethernet,
  adapters, saves, free space, and protected drives before choosing a path.
- Request permission before a system performance/load test. Explain its load,
  duration, and limits. Honor permission already given in the current session.
- Identify a queued PS4 system update before helping remove it. Leave game
  updates and saves alone. Do not silently update firmware or reset a console.
- Verify current primary sources. Do not turn a browser bug's affected range
  into a promise of full jailbreak support for every version in that range.
- Keep loader success, package transfer, installation, app launch, and actual
  gameplay as separate checks. Ask what the console shows when you cannot see.
- Do not format drives or change unrelated network settings as a shortcut.
  My external SSD is off-limits: do not inspect, mount, read, or write it.

## Code and delivery

- Use Graft first for code context. If it cannot index a language or source,
  say so once and use focused source reads. Do not keep retrying weak queries.
- Make code changes in an isolated Git worktree. Preserve other worktrees.
- Run CONTRIBUTING.md checks locally. Never create, trigger, monitor, or wait
  for GitHub Actions.
- Commit finished changes. Merge or publish only when I directly ask. Current
  session permission does not become blanket permission for future sessions.
- Review staged files and history. Keep games, firmware, keys, saves, emulator
  bundles, credentials, local agent config, and raw logs out of Git.
- After each commit, refresh one short completion note here.

## Performance guardrails

- Keep 1080p / 60 cap / perf 3 as the working baseline. The 900p boss trial
  felt worse and was rolled back. Bigger FPS text was not a speedup.
- profile_runtime.py measures CPU/GPU activity, not FPS or scene state.
  Use light recordings during play; keep heavy Metal/Instruments tracing off.
- Back up saves for experiments. Prefer separate emulator settings and copied
  saves, and never test through my only copy of a save.
- Measure the same scene and route. Check frame times, game speed, controls,
  sound, visuals, and crashes. A higher cap or a dry run cannot prove 90+ FPS.
- Work order: measured Mac performance, Windows/Linux, then browser research.
  Browser-local execution versus streaming remains open.

## Completion note

2026-10-13: Added draw timing notes and four locked-input shader-reuse tests.
Enabled runs reached 50.63/50.44 FPS; controls reached 46.11/42.42. This is
promising, with background work still uncontrolled. 90+ FPS remains open.

## Tests still open

- Private Mesa `675da32` skips clean, unchanged shader binds. It builds and
  passes 10,000 old-method comparisons. Keep it off by default pending more
  scenes and combat, sound, controls, and game-speed checks.
- Private source `9239edb` adds the one-way F9 benchmark input lock. Its 65
  checks and live lock checks pass. Restart the test app to regain input.
  An earlier unlocked diagnostic moved and is invalid for speed comparison.
- Depth-state and descriptor caches have no repeatable FPS gain. Keep them
  private and off. Depth-state creation measured only 1.45% of wall time in
  one diagnostic. Optional probes and thread-priority changes stay off for
  normal comparisons. PERFORMANCE.md carries the earlier results.
- Keep the optional buffer patch off by default. Draw setup is the next
  lead. Mesa already skips replay copies for one-time command buffers;
  do not duplicate that work or skip barriers without proving correctness.
- Raw captures, exact source patches, build hashes, and the next trial stay
  in ignored runtime/optimization-state.json and nearby trial folders.
  All 16 original saves match their backups. The original config differs
  only in volume (100 to 0); leave it untouched. The external SSD remains
  off-limits. Check preservation again after each experiment.
- Preserve patch context spaces through .gitattributes and check patches
  with git apply before sharing. Heavy tracing and debugger attachment
  remain off-limits for these runs.

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
