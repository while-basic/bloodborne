```text
Document:    Bloodborne Launcher Contribution Guide
Version:     v1.1.0
Author:      Christopher Celaya
Contact:     https://github.com/while-basic
Date:        2026-10-12
SHA256:      d1fdfcc4cf409a51b55390a5e24f0c936e5aef7ec4dce14db09145f52578c201
Chain:       solana-mainnet
Tx:          65Q2Brd2QEvAwyZo7hbkCWWWwii5LzWqoGqszXHhmhKxjjGLuVggcfih24WcufrKn67QEXM3ZvcLnoMZv8aUY8MQ
License:     The Unlicense (public domain dedication)
```

# Contributing

Bug reports, code contributions, setup feedback, and reproducible measurements
are welcome. This is Christopher Celaya's personal project at
[while-basic/bloodborne](https://github.com/while-basic/bloodborne).
Original project code and docs are released under [the Unlicense](LICENSE).
Contribute only work you have the right to share, under the same terms.

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
