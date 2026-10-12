```text
Document:    What I Want to Work on Next
Version:     v1.2.0
Author:      Christopher Celaya
Contact:     https://github.com/while-basic
Date:        2026-10-12
SHA256:      e38d724a121f717b00c67b49efa0faabdb232ccf743eb4a0478ae5201374dc71
Chain:       solana-mainnet
Tx:          gGaBqp5cmK6Dsw9CXdnudDF27anRVLmbTb45wjthfGodMFYMqsnimb2NNH1e3kbRwA6eFzN4nUuUYRAXE21w37S
License:     The Unlicense (public domain dedication)
```

# What's next

Right now I'm getting **24–55 FPS on my M5 Max with 128 GB of RAM**.
Here's the order I want to tackle things.

## 1. Get the Mac to 90+ FPS

This is the first goal. I mean 90+ while actually playing, not just choosing a
higher cap or catching one good frame on the counter.

Before I can compare changes properly, I need a repeatable test: the same
location, the same route, and the exact emulator build and patches written down.
I'll record resolution, quality settings, average FPS, lows, and stutters.
First visits to an area need their own runs because of shader compilation.

Then I can work through where the time is going: CPU emulation, graphics
translation, shaders, or frame pacing. I'll compare settings and upstream updates
one at a time, including whether they change how the game looks or plays.

I haven't settled on a target resolution and quality level for 90+ yet.
Some of this will depend on work in shadPS4 and the graphics drivers, so I
don't have a date for it.

## 2. Windows and Linux

After the Mac work, I want to get this setup working well on Windows and Linux.

That means fixing the platform-specific paths and launch steps, testing native
Vulkan drivers, and checking controllers, audio, fullscreen, and save/load.
I'll list the hardware and results for each system as I test it.
shadPS4 supporting a platform doesn't automatically mean this launcher is ready
for it.

## 3. The browser

Then I want to see what I can do in a web browser.

I haven't chosen between running it inside the browser and streaming it from
a computer. They're very different projects. Running it locally would need
a lot more work on the emulator, graphics, memory, and storage. Streaming
would still need a host computer and a look at input lag.

There's no browser build yet. I'll share what works when I have something
to show.

## Keeping track

For each update, I'll write down the build, settings, what changed, and what
I measured. I also want to check controls, audio, game speed, crashes, and saves.
More FPS isn't much use if the game stops working properly.

When sharing a result, include the Mac/PC specs, OS and driver versions, emulator
build/hash, patch XML hash, game region/update, power mode, display refresh rate,
resolution, FPS cap, and enabled patches. Keep saves and private logs local.

**October 12, 2026:** Published the Mac launcher, setup instructions, and prompts
you can give your agent. Current gameplay is around 24–55 FPS. Mac 90+ comes first,
then Windows and Linux, then the browser.
