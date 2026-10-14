```text
Document:    My Bloodborne Agent Guide
Version:     v2.15.0
Author:      Christopher Celaya
Contact:     https://github.com/while-basic
Date:        2026-10-13
SHA256:      816afae6a822992f3c2717bcff4f20686681f511022bacdb163cb5ed8b814a73
Chain:       solana-mainnet
Tx:          5HPGwDFCcCy8rkVmfkmMxBiapkdkiJuFufiV8pqVgNArTGHtPdsBdWfDHHy3HTaRJBVane5E6xerCs1Uv3gDosCm
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

2026-10-14: I stopped at a clean checkpoint after publishing the frame-clock
fix, measuring buffer work, and rerunning GPU feedback with an explicit log.
The retry produced 13,459 error-free GPU rows; its short automated route had
0.31 ms mean and 1.63 ms maximum GPU command residence after load. That is a
diagnostic lead, not a gameplay result or a 90+ FPS claim. All test apps are
closed, all 16 original saves and current settings match, and 90+ FPS remains
unverified. I also tried `Immediate` present mode on the same automated route:
about 103 FPS versus about 101 FPS with the prior setting. I kept the public
default unchanged because this route is not a busy gameplay scene.
The CPU recorder still points at `GpuCommandProcessor` and `Game:Main`, not the
present thread. A five-second macOS `sample` attempt on the Rosetta process
exited without a stack file, so I made no function-level CPU change.

2026-10-14: I rewrote the PS4-to-Mac walkthrough in clear first-person steps.
It now asks about gear and firmware first, separates USB from Ethernet, and
keeps the exact-firmware gate for 13.xx paths.

## Resume from here

- I asked to stop this session. Do not start another benchmark until I resume.
- My best repeated lighter-effects runs remain 71.11/71.34 FPS at 1080p.
  The new buffer diagnostics are separate from those runs.
- Private source `92ce9d8` adds optional normal-thread buffer timing. The Release
  build and Intel sanitizer checks pass. The same signed app completed both
  buffer-range trials; PERFORMANCE.md records the results and limits.
- Buffer fetch calls occupied 16–19% of the diagnostic windows. Nested times
  overlap and include probe overhead; they are not CPU or GPU usage figures.
- My next lead is existing Metal GPU start/end feedback in `kk_queue.c` and
  `mtl_command_queue.m`. I inspected it but made no change or GPU capture.
- The exact builds, private commits, trial paths, and preservation checks are
  saved in ignored `runtime/optimization-state.json`. Keep all probes off for
  normal FPS tests. The external SSD stays off-limits.

## Tests still open

- Private source `663fd82` counts memory faults and protection requests with
  lock-free counters. The Release build and signal/concurrency checks pass.
  Clock-aligned repeats counted about 122 versus 900 write faults per frame
  at 64 KiB versus the original range. Counts do not measure handling time.
  Normal-thread buffer work is now measured below; keep probes off for FPS tests.
- The public frame-clock patch builds and passes checks on the actual recorder,
  including stale-file refusal. Live clock gaps were under five microseconds.
  Runtime metadata keeps the exact signed builds and separates the later
  refusal guard from the clocked game runs. Fresh vblank tests show no gain.
- Private source `25f90df` counts short SSE4a and patcher events.
  The build, sanitizer, concurrent-counter, and live-signal checks pass.
  All four counters stayed at zero across 59.09 seconds in the lamp scene.
  It stays off by default. No signal handler logs or reads a clock.
  The existing presentation probe remains a separate dirty edit.

- Private Mesa `f99a9bd` reuses unchanged vertex binds. The build and 40,000
  old-method checks pass, but the pair fell from 56.28 to 45.89 FPS with stalls.
  Keep it private and off. Live counters avoided new dirty marks on 7.03% of calls;
  they do not prove later GPU uploads were skipped.
- Locked 1080p effects tests reached 56.28/56.38 FPS at perf 3 and 71.11/71.34
  at perf 7. Shader reuse stayed on; vertex reuse and probes stayed off. The
  lighter picture is a tradeoff. One 720p trial reached 73.75; 90+ is unverified.
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
- Keep the optional buffer patch off by default. GPU completion timing is the next
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
