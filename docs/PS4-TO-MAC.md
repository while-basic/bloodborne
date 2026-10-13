```text
Document:    My Bloodborne PS4 to Mac Walkthrough
Version:     v1.0.0
Author:      Christopher Celaya
Contact:     https://github.com/while-basic
Date:        2026-10-13
SHA256:      f3deb1c56b8e4414ecae7b608c13cca1e26d21c663331203d32cfa9f3e6819c3
Chain:       solana-mainnet
Tx:          2RGxEFTkB3gkrF6J2p5uHVZcnAmXRLLdvK1dwku5hRbmXfGVPwh8t6GXd4GWD93DsqdhJvZVgXYx3HfhezaECi2Z
License:     The Unlicense (public domain dedication)
```

# From my disc to my Mac

I started with a PS4, my Bloodborne disc, and a lot of questions. Codex and
Claude helped with the Mac work and walked me through the console screens.
This is the route, with stops to check that each part worked.

**First move:** open this repo in Codex or Claude and paste the
[disc-to-Mac prompt](AGENT-INSTALL.md#start-with-my-disc-and-ps4).
Ask for one step at a time. You do not need to know every term before you start.

## 1. Lay the gear on the table

I want the agent to ask these questions before choosing a method:

| Question | Why I ask |
| --- | --- |
| Which Mac, chip, RAM, and macOS version? | Check the current emulator requirements. |
| How much space is free on the chosen drive? | Keep room for the game, backup, update, and cache. |
| What exact PS4 firmware? | Each homebrew method supports specific versions. |
| Disc or digital copy? Which region and update? | This launcher uses CUSA00900 / 01.09. |
| Is GoldHEN already working? | Skip work that is already done. |
| Do you have a spare USB drive? What is on it? | Copying files and erasing a drive are different jobs. |
| Ethernet cable? USB-C Ethernet adapter? Router? | Pick a network path that fits the gear. |
| Controller and working data cable? | Check input on both the PS4 and Mac. |
| Are saves backed up? Which drives are off-limits? | Keep the good stuff safe. |

On the PS4, read **Settings → System → System Information**. Write down the
full number. `11.00` and `11.02` are different versions.

Before testing the Mac, the agent should ask:

> May I run a short local Mac check? I'll read the chip, RAM, OS, free space,
> and display settings. Before any load test, I'll explain its length and
> what it runs. It may use more power and raise fan noise. Results stay local.

You can say no and keep going with the guide. Specs can rule out missing
requirements, but no quick CPU test can promise Bloodborne will run well.
After setup, a short gameplay test gives much better evidence.

## 2. Stop the surprise system update

I keep the console off the internet while checking this part.

1. Open **Notifications**, then **Downloads** if that view is shown.
2. Look for a queued **System Software** update. Have the agent help identify
   that exact item. Do not select Bloodborne's game update.
3. If a system update is queued, highlight it, press **OPTIONS → Delete**, and
   check it is gone. This removes the downloaded update; it does not downgrade
   the firmware already installed.
4. Open **Settings → System → Automatic Downloads** and clear **System
   Software Update Files**. Leave unrelated settings alone.
5. Do not choose System Software Update, Initialize PS4, or a full-system
   restore as part of this guide.

Sony documents the [notification update-file deletion step](https://www.playstation.com/en-ca/support/error-codes/ps4/su-41350-3/).
I'm using only that cleanup step here, not its later update instructions.
If an agent can operate the console, it must explain the exact deletion and
get the required approval first. On my setup, I handled the PS4 buttons.

## 3. Pick a firmware path

I checked these primary project guides on **October 13, 2026**. Support can
change. Have the agent open the current guide and check the exact version,
required entry point, and matching homebrew payload before running anything.

| Route | What its own guide says | What to check |
| --- | --- | --- |
| [CSSFontFace + Lapse](https://github.com/ntfargo/CSSFontFace-Exploit) | Full PS4 chain lists 7.00–11.02. | Browser setup and a matching payload. This is the family of loader I used on 11.02. |
| [PPPwn](https://github.com/TheOfficialFloW/PPPwn) | Exploit covers firmware through 11.00; implemented versions are listed in its README. | Supported exact version, Ethernet, host tools, and matching payload. It does not cover my 11.02 setup. |
| [Vue After Free](https://github.com/Vuemony/vue-after-free) | Its tested jailbreak range is 7.00–13.00. | Required Vue app/save setup; some install paths erase console data, so do not choose those by default. |
| [HenLoader LP](https://github.com/GoldHEN/henloader_lp) | Lapse 9.00–12.02; Poops 9.00–13.00. | BD-J disc requirements, Blu-ray activation, and exact payload support. |

A browser bug working on a firmware is not the same as a full jailbreak
working on it. For example, the CSSFontFace page lists a wider bug range than
its working chain. I could verify the routes above through 13.00, **not a
blanket claim for every 13.xx version**. For newer firmware, stop at this gate
until a primary project documents a complete supported route. Do not update
the console just to try to match this table.

My local run used a CSSFontFace/Lapse loader with a matching GoldHEN payload.
I used Ethernet to reach a page hosted on my Mac. That was not PPPwn.

## 4. USB or Ethernet? They do different jobs

| Gear | What I can use it for |
| --- | --- |
| USB storage drive | Carry a homebrew PKG, a payload when the chosen method needs one, or a game dump. |
| Ethernet cable | Reach a local loader, send packages, or transfer a game backup. Some methods also use Ethernet for the exploit itself. |
| USB-C Ethernet adapter | Give the Mac an Ethernet port. It is not a USB storage drive. |
| Home router | Put both devices on the same local network, when that route fits. |

I connected **Mac USB-C → Ethernet adapter → Ethernet cable → PS4 LAN port**.
That direct link kept transfers local. I did not need to erase a storage drive
just to use Ethernet.

For a direct link, have the agent walk through this:

1. Identify the actual Ethernet service on the Mac. Save its current settings.
   Do not guess an interface name such as `en8`.
2. Choose a free private subnet that does not overlap Wi-Fi, a VPN, or another
   active network. My example used `192.168.50.0/24`; yours may need another.
3. In the Mac's **System Settings → Network → the Ethernet adapter → Details
   → TCP/IP**, set IPv4 manually. Example: Mac `192.168.50.1`, mask
   `255.255.255.0`.
4. On PS4, open **Settings → Network → Set Up Internet Connection → Use a LAN
   Cable → Custom**. For this direct browser/transfer path, choose a manual
   address, such as `192.168.50.2`, with the same mask. Set gateway/DNS only
   as required by the verified local host setup. If using the Mac address for
   those fields, the agent must explain that it does not create internet or
   DNS service. Keep MTU automatic and proxy off unless the chosen guide says
   otherwise. Do not pick PPPoE for this path.
5. Check the local link. A PS4 internet test may fail on a local-only cable
   while the Mac and PS4 can still reach each other. Check the actual loader
   page or service, not just the internet test.
6. Have the agent start the chosen, reviewed loader on the Mac and give the
   exact local URL, protocol, and port. Open it in the PS4 browser. Follow
   that project's steps; do not turn off security checks to hide an error.
7. Record how to restore the old network settings. Do not enable Internet
   Sharing or bridge the PS4 onto another network without a separate reason.

For USB, first identify the drive by name, size, and what it contains. Back it
up. Use the format required by the chosen tool; many expect exFAT with MBR.
**Do not format a drive without a clear choice and approval.** A spare drive
is far cheaper than losing a backup.

## 5. Load homebrew, then check it worked

1. Keep saves backed up. Follow the selected project's exact loader and
   payload steps for your firmware. Some routes need a USB payload or disc;
   some browser routes can serve the payload from the Mac.
2. Wait for the success message and the **GoldHEN** menu on the console.
   A Mac server saying “listening” only means the server started.
3. If using network transfer, enable GoldHEN's FTP server and test its actual
   connection on the PS4's address. GoldHEN documents port **2121**. Keep it
   on the trusted local link.
4. If the console crashes, follow the selected tool's recovery steps. After
   a full restart, expect to load GoldHEN again. Do not treat it as a permanent
   firmware install.

See [GoldHEN's own feature list](https://github.com/GoldHEN/GoldHEN) for its
package installer and FTP support. The homebrew package comes **after** this
step; installing a random PKG is not a way to jailbreak a stock PS4.

## 6. Install the homebrew app

I used tools such as [Itemzflow](https://github.com/LightningMods/Itemzflow)
for the game-backup workflow. Get a PS4 release through the maintainer's links.
Check the package name and any published hash before copying it.

1. **USB path:** put the homebrew `.pkg` at the root of the prepared drive,
   safely eject it from the Mac, and connect it to the PS4.
2. **Ethernet path:** with GoldHEN active, use its supported package-transfer
   path. For its internal installer, transfer the completed PKG to
   `/data/pkg/` and verify the transfer. GoldHEN documents that directory.
3. Open **GoldHEN → Debug Settings → Package Installer**. Menu wording may
   vary by build; have the agent use the screen you actually see. Choose the
   intended homebrew package and wait for installation to finish.
4. Return to the PS4 home screen and open the app. Confirm its main screen
   appears. Copying a PKG and installing it are separate steps.

Use only the drive you approved. Itemzflow's upstream guide says its dumper
uses the first USB drive it finds. Disconnect other storage before that route.
If you cannot do that safely, pick a supported network-dump route instead.

## 7. Back up my own Bloodborne

1. Insert the disc and make sure the game is fully installed on the PS4.
   For a digital copy, verify your own installed copy. Keep the existing
   firmware; do not accept a system update prompt.
2. Verify the game's title ID and version. This wrapper's patches target
   **CUSA00900 / 01.09**. Back up the base game and the matching installed
   update separately, using the dumper's documented steps.
3. Choose the approved USB or network destination. Check free space before
   starting. Wait for the dumper's completion message and check its report.
4. Transfer the complete result to the Mac's chosen folder. Check file counts,
   sizes, and hashes where available. Keep the source copy until the Mac copy
   has passed these checks.
5. Follow shadPS4's current guide for required modules from your own console
   and for importing the dump/update. Plain encrypted files copied over FTP
   are not necessarily an emulator-ready dump.
6. Keep saves in a separate backup. Do not mix a save restore into an FPS test.

I do not bundle the game, updates, firmware, or keys. There are no game download
links here. A different region needs its own compatible setup; renaming the
folder will not fix it.

## 8. Launch on the Mac

Follow [Mac setup in the README](../README.md#mac-setup), or paste the
[extracted-game prompt](AGENT-INSTALL.md#i-already-have-my-extracted-game).
Run `python3 play.py --check` first, then launch the 1080p / 60 cap / perf 3
baseline. Check the title screen, controls, sound, and a short walk in the game.

Once that works, ask about a measured FPS test. Agree on a scene, picture
quality, and test length. Keep one working profile to return to. Do not turn
every knob at once. Even hunters need a way home.
