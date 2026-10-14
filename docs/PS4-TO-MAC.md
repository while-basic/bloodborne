```text
Document:    My Bloodborne PS4 to Mac Walkthrough
Version:     v2.0.0
Author:      Christopher Celaya
Contact:     https://github.com/while-basic
Date:        2026-10-13
SHA256:      f56b78cacb1988fe73d6a75b24d04732e139156fc8c3498eff6641995a474f81
Chain:       solana-mainnet
Tx:          3PM6VCxEEoFN4FuwQM4yhfgvJKY89gNb86uwdMBHevP1bpNMFypKi28ZrTYdHKp7EeoFiMWzfj2A74mkPsdxS5Eh
License:     The Unlicense (public domain dedication)
```

# From my disc to my Mac

I started with a PS4, my Bloodborne disc, and a pile of questions. Codex and
Claude helped me with Mac commands and walked me through the PS4 screens. I
still pressed the buttons and checked what the console showed.

Open this repo in Codex or Claude and paste the [disc-to-Mac prompt](AGENT-INSTALL.md#start-with-my-disc-and-ps4). Ask for one short step at a time. You do not need to know every term before you start.

## 1. Put your gear on the table

Before choosing a path, I have the agent ask:

| Question | Why it matters |
| --- | --- |
| Which Mac, chip, RAM, and macOS version do you have? | I can compare it with current shadPS4 requirements. |
| How much free space is on the drive I may use? | The game, backup, update, and shader cache need room. |
| What exact PS4 firmware number is on the console? | A path for 11.00 may not work on 11.02. |
| Do you have the disc or a digital copy? What region and update? | My patches target CUSA00900 / 01.09. |
| Is GoldHEN already running? | I can skip steps you finished. |
| Do you have a spare USB drive? What is on it? | I never assume a drive is empty. |
| Do you have an Ethernet cable, a USB-C Ethernet adapter, or both? | This decides how the PS4 and Mac can talk. |
| Which saves, drives, and folders must stay untouched? | I write down the boundary before copying anything. |

On the PS4, read **Settings → System → System Information** and write down the full firmware number. `11.00` and `11.02` are different.

Before any Mac load test, the agent asks:

> May I run a short local Mac performance check? I will explain what it does, how long it runs, and what it cannot prove. It may use more power and make the fans louder. The result stays on this Mac.

You can say no. Reading the Mac specs is a check. It is not proof that a game will run well. A short, real gameplay route tells me much more.

## 2. Stop a surprise PS4 update

I keep the console off the internet while I check this part.

1. Open **Notifications**, then **Downloads** if that screen is shown.
2. Look for a queued **System Software** update. Show the agent the exact item.
3. Do not select a Bloodborne game update or a save file. If the system update is the item you want gone, ask the agent to explain it first, then highlight it and press **OPTIONS → Delete**.
4. Open **Settings → System → Automatic Downloads** and clear **System Software Update Files**. Leave other settings alone.
5. Do not choose **System Software Update**, **Initialize PS4**, or a full restore as part of this guide.

Deleting a downloaded update file does not downgrade firmware that is already installed. Sony's [notification support page](https://www.playstation.com/en-ca/support/error-codes/ps4/su-41350-3/) describes the menu. I use only the cleanup step here.

## 3. Check the exact firmware path

Firmware support changes. I checked the linked project READMEs on October 13, 2026. Check them again before you start, and make the agent show you the line that matches your exact firmware.

| Project | What its current README says | What I must check |
| --- | --- | --- |
| [CSSFontFace + Lapse](https://github.com/ntfargo/CSSFontFace-Exploit) | The listed PS4 chain is 6.00–11.02. | Browser setup, matching payload, and the exact firmware. This is the family I used on 11.02. |
| [PPPwn](https://github.com/TheOfficialFloW/PPPwn) | The kernel exploit is for PS4 firmware up to 11.00. | Exact supported version, Ethernet setup, host tool, and payload. It is not my 11.02 path. |
| [Vue After Free](https://github.com/Vuemony/vue-after-free) | Its README lists a 7.00–13.00 route, with different Lapse and Netctrl ranges. | The required app or save setup, payload, and any data-loss warning. |
| [HenLoader LP](https://github.com/GoldHEN/henloader_lp) | It is a loader, not a promise that every 13.xx release is jailbroken. | The release notes, payload, and exact firmware support. |

A browser bug range is not the same as a complete jailbreak range. I do not call every 13.xx version supported. I do not update the console just to match a table. If the current primary guide does not show a complete path for the exact version, I stop and keep the firmware where it is.

My local run used CSSFontFace/Lapse on 11.02. I used Ethernet to reach a loader page hosted on my Mac. That was not PPPwn.

## 4. Choose USB or Ethernet

They solve different problems:

| Gear | Good use |
| --- | --- |
| USB storage drive | Carry a homebrew PKG, payload, or game dump when the chosen guide needs it. |
| Ethernet cable | Reach a local loader and move files on a trusted local link. |
| USB-C Ethernet adapter | Give a Mac without an Ethernet jack a wired port. It is not USB storage. |
| Home router | Put both devices on the same local network when the chosen guide allows it. |

I used **Mac USB-C → Ethernet adapter → Ethernet cable → PS4 LAN port**. That kept transfers local. I did not format a drive for this cable.

For a direct cable, I have the agent walk me through this exact order:

1. Find the real Ethernet service on the Mac and write down its old settings. I do not guess an interface name such as `en8`.
2. Pick a private subnet that does not overlap Wi-Fi, a VPN, or another active network. My example was `192.168.50.0/24`; yours may differ.
3. In **System Settings → Network → Ethernet adapter → Details → TCP/IP**, set a manual Mac address. Example: `192.168.50.1`, mask `255.255.255.0`.
4. On the PS4, choose **Settings → Network → Set Up Internet Connection → Use LAN Cable → Custom**. For a direct local path, use `192.168.50.2` and the same mask. Add a gateway or DNS only when the chosen guide requires it. Keep MTU automatic and proxy off unless that guide says otherwise.
5. Test the loader page or file service. A PS4 internet test may fail on a local-only cable even when the Mac and PS4 can reach each other.
6. Have the agent start the chosen, reviewed loader and give me its exact local URL, port, and protocol. I open that URL in the PS4 browser.
7. Write down how to restore the old Mac and PS4 network settings. I do not turn on Internet Sharing or bridge networks for no reason.

For USB, I first check the drive name, size, and contents. I back up anything important. I use the format the chosen guide requires. I do not format a drive without a clear choice and a backup. A spare drive costs less than losing a good backup.

## 5. Load homebrew and check the result

1. Keep saves backed up. Follow the selected project's exact loader and payload steps for the firmware I checked.
2. Wait for the **GoldHEN** menu on the console. A Mac server that says “listening” only proves that the server started.
3. If I use a network transfer, enable GoldHEN's FTP server and test the real PS4 address on the trusted local link. GoldHEN documents port `2121`.
4. If the console restarts, I expect to load GoldHEN again. I do not treat this as a permanent firmware change.

The homebrew package comes after the loader works. Installing a random PKG is not a jailbreak for a stock PS4. I use the [GoldHEN project](https://github.com/GoldHEN/GoldHEN) and the selected app's own guide.

## 6. Install the homebrew app

I used [Itemzflow](https://github.com/LightningMods/Itemzflow) for my game-backup workflow. I get releases from the maintainer's links and check the package name and hash when one is provided.

1. **USB path:** put the approved `.pkg` on the prepared drive, safely eject it, and connect it to the PS4.
2. **Ethernet path:** keep GoldHEN active and use the supported package-transfer method. If the guide uses `/data/pkg/`, verify the completed transfer before installing.
3. Open **GoldHEN → Debug Settings → Package Installer**. Menu names can differ by build, so I use the screen I actually see.
4. Wait for the install to finish. Return to the PS4 home screen and open the app.

Copying a PKG and installing it are two different steps. Itemzflow may use the first USB drive it finds, so I disconnect other storage before a dump. If that feels unsafe, I use a supported network-dump path instead.

## 7. Back up my own Bloodborne copy

1. Insert my disc and let the PS4 finish installing it. A digital copy must be mine and already installed.
2. Check the title ID and update. This launcher targets **CUSA00900 / 01.09**. I keep the base game and update records clear.
3. Choose an approved USB or network destination and check free space first.
4. Run the dumper's documented steps. Wait for its completion message and verify the copy with file sizes or hashes when possible.
5. Follow the current [shadPS4 setup guide](https://shadps4.net/) for required modules and import rules. A plain FTP copy of encrypted installed files may not be an emulator-ready dump.
6. Keep saves in a separate backup. I never mix save restore into an FPS test.

I do not share game files, updates, firmware, keys, or download links. A different region needs its own compatible setup; renaming a folder does not fix it.

## 8. Set up the Mac

Follow [the Mac setup in the README](../README.md#mac-setup). The short version is:

1. Install Python 3.11 or newer and the shadPS4 Qt Launcher.
2. Install the pre-release shadPS4 engine, open it once, then close it so the config exists.
3. Put my complete extracted game under `runtime/games/CUSA00900/` and keep the original backup.
4. Download the matching [Bloodborne patch file](https://raw.githubusercontent.com/shadps4-emu/ps4_cheats/main/PATCHES/Bloodborne.xml) into `runtime/downloads/Bloodborne.xml`.
5. Close shadPS4, back up the config, saves, and any generated patch profile.
6. Run `python3 play.py --check`. This checks local files. It does not launch the game or prove gameplay.
7. Launch with `python3 play.py`, or use `Play Bloodborne.command`.
8. Check the title screen, controls, sound, and a short walk. I report those checks separately from setup and FPS.

Once that works, I agree on one scene, picture quality, and test length before measuring FPS. I keep the 1080p / 60 cap / perf 3 profile as my way home.

## If I get stuck

I tell the agent the exact screen, error, firmware, game update, Mac model, and cable path. I do not delete caches, reset the PS4, update firmware, or format a drive as a first guess. The [starter prompts](AGENT-INSTALL.md) and [performance notes](../PERFORMANCE.md) keep the next step small.
