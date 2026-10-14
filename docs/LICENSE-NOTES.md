```text
Document:    My Bloodborne Launcher License Notes
Version:     v1.4.0
Author:      Christopher Celaya
Contact:     https://github.com/while-basic
Date:        2026-10-14
SHA256:      59ebfc6ae8277ee2c9c9b27c3b51263ce0329fb9034fb6661d83580d4ddbbf25
Chain:       solana-mainnet
Tx:          4j28Msvcp14mG2E2VnY72VfgypseYo5VxrDdpx7CRKqjfi7qBXeV5D9fKcLZbQ958juz5GBX6JVCeJHNXcapbyxN
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
GPL-2.0-or-later. I do not include its app in this repo, and my
Unlicense dedication does not cover it. The crash fix under `patches/bbport/`
changes bbport code, so it follows bbport's GPL-2.0-or-later license too.
