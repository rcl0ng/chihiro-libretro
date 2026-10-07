# Chihiro setup and limitations

## BIOS / paths

Find RetroArch Settings → Directory → System/BIOS. Make a `chihiro` subfolder there. The required filenames recorded by the core are:

```
chihiro/chihiro_xbox_bios.bin
chihiro/fpr21042_m29w160et.bin
chihiro/ic10_g24lc64.bin
chihiro/ic11_24lc024.bin
chihiro/pc20_g24lc64.bin
```

OutRun 2 Special Tours additionally uses `chihiro/ver1305.bin`. No Chihiro/Xbox firmware is bundled. Do not rename an arbitrary BIOS to satisfy the filename; use the correct image required by the upstream Chihiro fork. Existing HDD/EEPROM/save data should be preserved and backed up. Load the game BIN as content; no `-dvd_path` command-line argument is required for libretro content loading.

## Input

Use frontend Port 1/2 with separate devices. For Wiimotes follow `INPUT-SETUP.md` including Lichtknarre, vJoy, dinput, button mapping, sensitivity/deadzone and Disable Left Analog in Menu. Select the available custom analog-gun device for gun play; retain the normal joypad device for gamepad games. Input descriptions change to fit recognized game profiles. With an XInput pad choose the appropriate RetroArch input/joypad driver for that pad rather than installing the vJoy profile.

| Game/profile | RetroPad controls |
|---|---|
| All cabinets | Start, Select coin, L3 Test, R3 Service |
| Virtua Cop 3 | Left X/Y aim, B trigger, A offscreen reload, X body action, Y pedal/bullet time |
| HOTD3 | Left X/Y aim, B trigger, A shotgun pump/reload |
| Ghost Squad | Left X/Y aim, B trigger, A offscreen reload, X body action, Y weapon change, D-pad Up insert card |
| OutRun 2 / SP | Left X steering, R2 accelerator, L2 brake, L/R gear down/up, Y view |
| Maximum Tune | Left X steering, R2 accelerator, L2 brake, L/R gear down/up latch, Y view, X intrude, D-pad Up insert/take card |
| Crazy Taxi | Left X steering, R2 accelerator, L2 brake, B Drive latch, A Reverse latch, Y jump |
| Ollie King | Left X board swing, L2/R2 or D-pad Up/Down foot sensors, B/L left grab, A/R right grab |

For Wiimote physical labels use the shared mapping table: RetroPad X=1, Y=2, B=Wiimote B, A=Wiimote A. The short Wiimote profile has no L3/R3 bindings; temporarily bind keyboard/pad buttons to Test/Service for calibration.

## Graphics and widescreen

**Vulkan is strongly recommended** and passed the maintainer’s tests. Choose a supported backend in RetroArch and restart the process before testing. Core Options → Video → **Widescreen Hack (Restart Required) → On (Supported Games)** enables the recognized profiles; default is Off. Let RetroArch use the core-provided aspect ratio. Start a new process after changing it. Unknown executable revisions remain unpatched. HUD/menu positions are not universally corrected. Change crosshair size independently for P1/P2 in Video options.

## Calibration / cards

Use Cabinet Test (L3) and Service (R3). On Maximum Tune enter the **Game Test submenu**, find its steering calibration and complete it; a JVS test showing left/center/right values does not itself calibrate the game. Steering stuck left/right in menus can be a calibration issue.

VC3: enter Game Test → Gun Adjustment. Follow the five targets (top/left/center/right/bottom), advance using Start/Service as required, place the displayed crosshair on each target and pull the trigger for each player. Exit both test menus back to gameplay. HOTD3/Ghost Squad also need their in-game gun calibration after display/aspect changes; The maintainer reported all three calibrated successfully. Test center and both edges before play.

Core Options → Input includes card insertion and saved/new-blank choices. Ghost Squad has P1/P2 cards; Maximum Tune has one card option with distinct per-game saved cards. Use D-pad Up to insert/take at the appropriate prompt. Cards are stored below the save directory's `chihiro` subfolder, with `cards.ini` and a `cards` directory. Example from maintainer testing: if the frontend's save base is `<RetroBat>/saves/chihiro`, cards.ini was at `<RetroBat>/saves/chihiro/chihiro/cards.ini`. Actual paths depend on frontend save sorting. Check the startup log's **Card directory base** instead of assuming one absolute path. Create a missing cards directory if necessary; preserve existing cards.ini and card files.

## Exit and reports

Final v15 load/exit was reported working. One game per RetroArch process remains a limitation; use Quit RetroArch rather than attempting another content load in the same process. Menu/exit hotkeys belong to RetroArch/AHK and are not assigned here. For a failure enable RetroArch file logging before launching, capture the current log plus versions and exact game revision; do not send ROM/BIOS files in public bug reports. Historical README references to a debug BAT do not apply: the uploaded v15 package did not contain that launcher, so v1.0.0 makes no claim to include it.
