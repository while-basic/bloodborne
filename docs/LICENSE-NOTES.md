```text
Document:    My Bloodborne Launcher License Notes
Version:     v2.0.0
Author:      Christopher Celaya
Contact:     https://github.com/while-basic
Date:        2026-10-21
SHA256:      7cab2cd12468e4e3fe85259ee609e6d943e4bb1999d95a8e522d12c8e131bb03
Chain:       solana-mainnet
Tx:          3hwYrDTSE59AB7FPzcaXVasJq6rBaiERwDBkVfbgwZJY8p5ce526TUxFr9NmEJgYoGZzLdkXZRVLeukYjydrQqYK
License:     The Unlicense (public domain dedication)
```

# Use it, change it, share it

I release my original code, tests, and docs under [the Unlicense](../LICENSE).
That includes my earlier original contributions. I keep the standard text
from [unlicense.org](https://unlicense.org/UNLICENSE) unchanged in LICENSE;
its document header lives here instead.

This does not cover Bloodborne, bbport, shadPS4, their assets, or other people's
tools. Their rights and licenses still apply. My work comes with no warranty.

`python3 play.py --install` downloads [bbport for Mac](https://github.com/bmy/bbport-mac)
from its official release page and checks the archive's SHA-256. The app stays
under ignored `runtime/`; it is not included in this repo. bbport and the
patches under `patches/bbport/` follow **GPL-2.0-or-later**, not my Unlicense
dedication. Their license text stays beside the patches.

The CSR tools use [SoulsFormats](https://github.com/JKAnderson/SoulsFormats)
and [JPEXS FFDec](https://github.com/jindrapetrik/jpexs-decompiler) as separate
dependencies. Keep their licenses and credits when distributing those tools.
Do not include edited game files, fonts, textures, or saves in a public fork.
