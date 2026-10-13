```text
Document:    My Bloodborne Agent Guide
Version:     v2.6.0
Author:      Christopher Celaya
Contact:     https://github.com/while-basic
Date:        2026-10-13
SHA256:      4adef1371c7e8840f41c7190e26905cdf8c9284e1fbfc1f812b72b1a3e60ef1d
Chain:       solana-mainnet
Tx:          3KQosXsTiBUFfDTMjsEDQbQREGBMjuMot1Wxokiu35grgnVD6jfE4AbngmLZvSpi6rNFXtDfnKeumvsYSYSNi6jz
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

2026-10-13: Published repeated driver-cache and effects tests, then measured
depth-state creation at 1.45% of wall time in one scene. Cache reuse works,
but no FPS gain is proved. Original saves and settings are intact; 90+ FPS is open.

## Tests still open

I tried reusing unchanged driver tables in a private Mesa build. Off/on/off
captures averaged 27.63/50.74/54.77 FPS, so I kept reuse off. Private commit
`b7f7574` saves that experiment; 30 method checks pass, including reset handling.

Private Mesa commit `1f83229` adds a small depth/stencil state cache, off by
default. It passed 36 checks and 20,000 threaded lookups with memory checks,
and the Intel driver builds. Off/on/off/on lamp captures averaged
29.55/55.54/50.15/42.16 FPS. No gain is established. All four used matching
driver, executable, game-patch, and starting-config hashes. Lamp endpoints
were checked. Initial keyboard checks failed to move the character.

Private commit `d387faf` adds an optional once-per-second depth-state probe.
It builds and passes 49 checks plus 20,000 threaded lookups. Creation took
1.45% of wall time in the control; the enabled run had 100% hits and 0.12%
lookup time. Keep the cache private and off; this is a small measured cost.
Diagnostic FPS averaged 30.63/21.89, with a 5.05-second stall in the second
run. Probe cost and background load were not controlled. Walking and camera
checks passed in both runs after clicking inside the game surface. Combat,
sound, and game speed remain open. Both diagnostic apps are closed.

Keep the optional buffer patch off by default. My 16 KiB repeats had stalls;
background load was not held constant. Immediate display mode and vblank 240
showed no clear gain. Measure logger overhead and a repeated busy route next,
including combat, sound, game speed, and picture quality.

Private source commit `2e603c5` saves the renderer and thread-priority probes;
leave them off during comparisons. Draw command recording is the next lead.
Mesa already skips replay-queue copies for one-time command buffers, which
the renderer uses; do not add a second version of that optimization.
ThinLTO stalled at startup. A manually moved trial is invalid and its copied
save stays private. Raw captures and exact test state stay in ignored runtime/.
All 16 original saves and my original config were checked unchanged.
Patch files keep needed context spaces through .gitattributes; check them
with git apply before sharing.

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
