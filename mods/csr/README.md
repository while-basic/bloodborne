```text
Document:    My CSR Bloodborne Mod
Version:     v1.1.0
Author:      Christopher Celaya
Contact:     https://github.com/while-basic
Date:        2026-10-21
SHA256:      3895f434cd044671ad5677a7a1046946f263d3575e6fd5ca1a7fddfeedb6486d
Chain:       solana-mainnet
Tx:          58sjH8D9nHu6ebDpiJ8zkVUzBuCknSTCVjqQKBvgNqGiaAFCv8PbgSXsqsetyi6RrJLnVyCJvtsD6J2HWQuKugeo
License:     The Unlicense (public domain dedication)
```

# A slightly less serious hunt

I renamed three weapons in my CUSA00900 / 1.09 copy:

| Original | New name |
| --- | --- |
| Saw Cleaver | Yharnam Can Opener |
| Hunter Axe | Eviction Notice |
| Threaded Cane | Gentleman’s Disagreement |

The US and UK English name tables each get 99 edits. That includes every
upgrade from +0 through +10, plus Lost and Uncanny versions. Those labels stay.
Stats, saves, descriptions, and the other text tables stay unchanged.

Both normal loading menus get a small `CSR · Celaya Solutions` label at the
bottom right. It uses the game's existing font and muted gold-gray text.
The patch adds two tags to each menu and preserves every original tag byte
for byte, including the animation and scripts. It does not replace credits.

## Build from your own files

You need .NET 8, Java 17, and Python 3.11 or newer. The name tool uses
[SoulsFormats 1.0.1](https://github.com/JKAnderson/SoulsFormats) from NuGet.
It targets an older .NET framework, so restore prints NU1701; the actual
Bloodborne archive and text read/write paths passed the checks below.

Download [JPEXS FFDec 26.4.0](https://github.com/jindrapetrik/jpexs-decompiler/releases/tag/version26.4.0)
as `ffdec_26.4.0.zip` and unpack it locally. Its SHA-256 is
`56ce960aeafc7caf034e2052ba49f878a883f7c7ca690da6eeffca9587b5e4b9`.
No game files or third-party binaries belong in this repo.

From the repo root, set these three paths to your local files:

```sh
CSR_GAME=/path/to/merged-1.09-game
CSR_OUT=/path/to/new-csr-overlay
CSR_FFDEC=/path/to/ffdec.jar
dotnet build mods/csr/WeaponNames
dotnet mods/csr/WeaponNames/bin/Debug/net8.0/WeaponNames.dll --self-test
for lang in engus enggb; do
  dotnet mods/csr/WeaponNames/bin/Debug/net8.0/WeaponNames.dll \
    "$CSR_GAME/dvdroot_ps4/msg/$lang/item.msgbnd.dcx" \
    "$CSR_OUT/dvdroot_ps4/msg/$lang/item.msgbnd.dcx"
done
for menu in nowloading nowloading2; do
  python3 mods/csr/brand_loading.py \
    "$CSR_GAME/dvdroot_ps4/menu/$menu.gfx" \
    "$CSR_OUT/dvdroot_ps4/menu/$menu.gfx" "$CSR_FFDEC"
done
```

Both tools refuse to overwrite an existing output. They reopen and verify
their output before writing it. The name tool requires all 99 expected names;
the menu tool requires the game's uncompressed 1920 × 1080 GFX v11 format.
Use a new output directory to rebuild.

On this Mac I installed the four files in a separate APFS clone at
`runtime/mods/csr/game`, with a copied save/config under `runtime/mods/csr/data`.
`runtime/mods/csr/Play CSR Bloodborne.command` launches that copy with the
existing bbport release. The normal launcher, game, settings, and saves stay
separate. Use the normal launcher to return to the original game.
The CSR save is its own copy; later progress does not sync back automatically.

## What I checked

- The Python suite passes, including malformed GFX input checks.
- The C# self-check covers all variants, Unicode, unchanged lore/null entries,
  and refusal when an expected weapon is missing.
- Both real English archives reopen correctly. The other 17 files in each
  archive retain their exact contents; only weapon-name table 11 changes.
- All 22 original tags in `nowloading.gfx` and all 459 in `nowloading2.gfx`
  remain byte-for-byte intact. Both new labels pass FFDec readback.
- FFDec renders the label at the bottom right using the game's English font.
  Its preview has missing-texture placeholders, so it is not a game screenshot.
- The copied game starts a bbport process. The screen-control tool cannot
  address that standalone window, so inventory text, clipping, loading-screen
  appearance, and continued play still need a human in-game check.

I stopped the test process. I did not install this on a PS4 or build new PKGs.
Keep the original game and save backups when trying it on other setups.
