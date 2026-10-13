```text
Document:    Contributing to Bloodborne on Mac
Version:     v1.3.0
Author:      Christopher Celaya
Contact:     https://github.com/while-basic
Date:        2026-10-13
SHA256:      84193a81887c05c06804f985b6065329719b2e5cd5924cc47f4a6c99dcf2d06b
Chain:       solana-mainnet
Tx:          2unyrLdw4PcUvunL8taqPAkfDbhPjzjRUfdPGpLE9r7uaTsuqYm5uNyfbGNGTjzv1DzextEDTv2pxxfXUZ5jdk4E
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
python3 -m py_compile play.py profile_runtime.py analyze_frames.py
python3 play.py --help
python3 analyze_frames.py --help
git diff --check
```

The tests don't need a game or emulator install. If your Mac is set up, also run
`python3 play.py --check`. That checks local files and patches without changing
settings. Say separately whether you actually launched and played the game.

I run checks locally. Please don't add GitHub Actions workflows.

For frame measurements, see [my capture guide](docs/FRAME-CAPTURE.md).
Use an observed gameplay interval and keep raw captures private. The analyzer
does not know whether a frame came from a menu or a fight.

Before pushing, check the files you're committing and the Git history for game
data, binaries, credentials, and private logs. Ignore rules won't remove
something that's already committed. Keep credits and license notices for
other people's work.
