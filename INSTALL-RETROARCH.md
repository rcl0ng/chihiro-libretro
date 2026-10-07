# Standalone RetroArch installation — Windows x64

RetroBat is optional. A fresh standalone RetroArch installation is the primary test environment for these packages.

1. Use Windows x64 RetroArch from https://www.retroarch.com/?page=platforms . Extract/install to a separate writable directory so your existing setup is preserved.
2. Open Settings → Directory and note the configured Core, Core Info, Controller Autoconfig, System/BIOS and Save Files directories. Close RetroArch.
3. Copy package `cores` contents into Core and `info` contents into Core Info. Do not put source archives there. Back up same-named custom files if upgrading; stock core filenames are separate.
4. For Wiimotes, install/configure Lichtknarre and vJoy separately. Copy `autoconfig/dinput/vJoy Device.cfg` into the configured Controller Autoconfig directory's `dinput` subfolder. Match its axis/button table exactly; see `docs/INPUT-SETUP.md`. With normal gamepads in Chihiro, skip the vJoy setup.
5. Restart RetroArch. For vJoy set Settings → Drivers → **Input = dinput** and **Controller/Joypad = dinput**, save configuration and fully restart RetroArch; choose each actual vJoy Device Index under Settings → Input → Port Controls. Set Analog to Digital Type None, sensitivity 1.0 and deadzone 0.0 for pointing devices.
6. **Settings → Input → Menu Controls → Disable Left Analog in Menu: ON.** This prevents IR movement driving the menus. Save configuration deliberately; do not assume launching through a different frontend retains the same configuration.
7. Use Load Core to select the custom DLL, then Load Content. FBNeo content is a matching intact ROM ZIP; if asked, load the archive with the core rather than exploring files inside it. Put required game/system BIOS where the relevant guide specifies. No games/BIOS are bundled.
8. Open Quick Menu → Controls and select the guide's Device Type, leaving frontend player-to-port mappings as documented. Save a Game Remap File. Save a Game Options File for game-specific core options. Old duplicate-device or port-routing remaps can override intended behavior.
9. Configure RetroArch Menu Toggle/exit hotkeys yourself. Home is not bound by the supplied vJoy profile. AHK is optional and not required to run the cores.

## First Chihiro test

Read docs/CHIHIRO-SETUP.md, install the required BIOS files, then load a previously working game BIN. Use an ordinary gamepad for driving/board games or the documented Lichtknarre/vJoy configuration for guns. Confirm aiming/calibration, controls, card persistence where relevant and normal exit. Start a new RetroArch process for each game. No RetroBat installation is required.

Optional RetroBat instructions and reference XMLs are isolated under `retrobat/`; ignore that directory for standalone use. BatGui identifies active config files; edit those directly rather than trying to reassign their source in BatGui.

## Recommended graphics backend

**Use Vulkan for Chihiro** (Settings > Drivers > Video), save configuration and restart RetroArch. Vulkan passed the maintainer’s tests. Start a fresh RetroArch process per game.
