```text
Document:    My Bloodborne Launcher License Notes
Version:     v1.3.0
Author:      Christopher Celaya
Contact:     https://github.com/while-basic
Date:        2026-10-13
SHA256:      72d219c0f74b32cda73ca0f46c1bad108a5a384346a52cdc40fcafae3c7988ee
Chain:       solana-mainnet
Tx:          4R1zBXMvLCNZwcFm5zBWJk4jbbj4KBDM7nXKKrdsn6EeRmgbgMPDe9fJiQj8b1WXsQrRZvmjdSQr5mi9LoJM6BzK
License:     The Unlicense (public domain dedication)
```

# Use it, change it, share it

I release my original code, tests, and docs in this repo under
[the Unlicense](../LICENSE). That includes my earlier original contributions.

I keep the standard text from [unlicense.org](https://unlicense.org/UNLICENSE)
unchanged in LICENSE so GitHub and other tools can recognize it. Its document
header lives here instead.

This does not cover Bloodborne, shadPS4, third-party patches, or their assets.
Their rights and licenses still apply. My original work comes with no warranty.

The frame-timing patch under `patches/shadps4/` changes shadPS4 and follows its
GPL-2.0-or-later license. It is outside my Unlicense dedication.

`python3 play.py --engine bbport --install` downloads
[bbport for Mac](https://github.com/bmy/bbport-mac) from its own release page
and checks the file's SHA-256 before unpacking it into `runtime/`. bbport is
GPL-2.0-or-later. I do not include its code or app in this repo, and my
Unlicense dedication does not cover it.
