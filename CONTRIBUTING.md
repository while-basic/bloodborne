```text
Document:    Contributing to Bloodborne on Mac
Version:     v2.0.0
Author:      Christopher Celaya
Contact:     https://github.com/while-basic
Date:        2026-10-21
SHA256:      e719b911000f28678ffc4e14ef0bcc92417ef429263dce8c4f38ed9c18e5b4aa
Chain:       solana-mainnet
Tx:          Lu4WvNXiSNLgDoPzs4mWEaELzxENuvAhtcxJ4zXtWVAHyfb62r5pfMdooVnPd2ZWn9HxoncGcGPRQRHsaFiU7Bg
License:     The Unlicense (public domain dedication)
```

# Want to help?

If you get this running, I'd like to know what you're using and how it performs.
If you fix something, send a pull request. Keep it small enough to explain.

My original code and docs use the Unlicense. The patches under `patches/bbport/`
follow bbport's GPL-2.0-or-later terms. Keep the upstream credits.

## If something breaks

Tell me your Mac chip, memory, macOS and Python version, exact bbport build,
game region/update, command, and what happened. For speed reports, include the
scene, settings, test length, and whether you had already visited the area.
Low frames and long pauses matter too.

Keep game files, saves, firmware, keys, passwords, and raw private logs out of
issues. Read what you're about to share before attaching it.

## Before sending a change

Use an isolated Git worktree. Run these checks locally with Python 3.11+:

```sh
python3 -m unittest discover -s tests -v
python3 -m py_compile play.py mods/csr/brand_loading.py
python3 play.py --help
git diff --check
```

For changes to the weapon-name tool, also use .NET 8:

```sh
dotnet run --project mods/csr/WeaponNames -- --self-test
```

The tests use temporary fixtures. They do not need a game or launch bbport.
On an installed Mac, also run `python3 play.py --check` and say separately
whether you actually played. Changes to a bbport patch need a local build
against its stated version and a check of the behavior it changes.

Use [the capture guide](docs/FRAME-CAPTURE.md) for frame reports. A CSV filter
cannot prove which scene you were in. Keep the raw evidence private.

I run checks locally. Do not create or run GitHub Actions workflows.
Before pushing, review staged files and Git history for private data, game
assets, and binaries. Ignore rules do not remove something already committed.
