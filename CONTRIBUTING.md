```text
Document:    Contributing to Bloodborne on Mac
Version:     v1.2.0
Author:      Christopher Celaya
Contact:     https://github.com/while-basic
Date:        2026-10-12
SHA256:      aed7f88affa3511d008d0923520f46057a87ef251c9b811377566e60a4d9ceb4
Chain:       solana-mainnet
Tx:          pq6K76oA4TS8XYTsnZ3DrDZ57tuvvWLBGNPfXcZjM3vo3E11dhZHjbez1gzZbaVSGtnyatWSnfpncRrvY8mdihw
License:     The Unlicense (public domain dedication)
```

# Want to help?

If you get this running, I'd like to know what you're using and how it performs.
If you fix something, send a pull request.

My code and docs are under [the Unlicense](LICENSE). Please only contribute work
you can share under the same terms.

## If something breaks

Open an issue with:

- Your computer, CPU/GPU, RAM, OS, and Python version.
- The exact shadPS4 build, game region/update, and patch file source/hash.
- The command you ran, what happened, and how to reproduce it.

For FPS results, include the scene, resolution, settings, and how long you tested.
Say whether you'd already visited the area and let its shaders compile.
Average FPS and lows help more than a single peak.

Keep passwords, tokens, personal details, game files, firmware, keys, and saves
out of issues. Read through logs before attaching them.

## Before sending a change

Run these locally with Python 3.11 or newer:

```sh
python3 -m unittest discover -s tests -v
python3 -m py_compile play.py
python3 play.py --help
git diff --check
```

The tests don't need a game or emulator install. If your Mac is set up, also run
`python3 play.py --check`. That checks local files and patches without changing
settings. Say separately whether you actually launched and played the game.

I run checks locally. Please don't add GitHub Actions workflows.

Before pushing, check the files you're committing and the Git history for game
data, binaries, credentials, and private logs. Ignore rules won't remove
something that's already committed. Keep credits and license notices for
other people's work.
