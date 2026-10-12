```text
Document:    Bloodborne Launcher Contribution Guide
Version:     v1.0.0
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-10-12
SHA256:      93ce4e827c5c7e1541f3fd343a0360c34351d5e57ba1c1493db42fa6fa7c9075
Chain:       solana-mainnet
Tx:          us59EmsqVxoPn8D57NHcdiwPJC52JvDThzYgaeFLnpWswUE7xTRq7XAioogh9Bq7NuLRqA8w4hxnfBQ3WYaciEe
License:     All Rights Reserved / Celaya Solutions
```

# Contributing

Bug reports, setup feedback, and reproducible measurements are welcome.
The source currently retains All Rights Reserved terms. A broader code
contribution policy will follow the maintainer's license decision.

## Report a problem

Include your OS/build, chip or CPU, GPU, RAM, Python version, exact emulator
version, game title ID/update, launch command, patch XML source/hash, and steps
to reproduce. For performance reports, give the scene, resolution, quality
settings, run duration, cold/warm cache state, average FPS, and lows.

Review logs before sharing: remove personal paths, account details, and other
private data. Do not upload game data, firmware, keys, saves, emulator bundles,
or links to unauthorized game downloads. Screenshots and videos are optional
and must be yours to share.

## Local verification

Python 3.11 or newer is required for the documented setup. No third-party Python
packages are needed.

```sh
python3 -m unittest discover -s tests -v
python3 -m py_compile play.py
python3 play.py --help
git diff --check
```

On a configured Mac, use `python3 play.py --check` to check local prerequisites
without launching or writing settings. Synthetic tests do not need game files
or an installed emulator. Neither test type proves gameplay performance.

All checks run locally. Do not create, run, or wait for GitHub Actions workflows.

## Before a public update

Review the staged file list and Git history for game files, binaries, secrets,
personal paths, and local agent settings. Ignore rules do not remove files
already committed or prevent forced adds. Keep runtime material outside the
source release. Credit external dependencies and retain their license notices.

Record the result of a real launch separately from automated checks. Update
the tested-build details and roadmap only when supported by evidence.
