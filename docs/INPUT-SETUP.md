# Wiimote / Lichtknarre / vJoy setup

The supported Wiimote pipeline is **Wiimote IR → Lichtknarre vJoy connector → vJoy X/Y and buttons → RetroArch DirectInput → custom core**. vJoy by itself does not track the Wiimote. The bundled autoconfig does not configure Lichtknarre or install a driver.

1. Install Lichtknarre from https://geekonarium.de/en/lichtknarre-lightgun/ and follow its official tracker, LED layout and calibration instructions. Use its vJoy connector, not its Windows mouse connector, for this setup.
2. Use a vJoy driver supported by your Lichtknarre distribution. Ron supplied the vJoy 2.1.9.1 installer and a Device Manager screenshot showing provider Shaul Eizikovich, date 2019-07-14, driver version 12.53.21.621, signer Microsoft Windows Hardware Compatibility Publisher. Installer and driver version numbers differ. This is the observed test setup, not a requirement that every user downgrade to it. It is not identified as a Nefarius release. Do not reinstall a working driver unnecessarily; an existing vJoy setup EXE can enter uninstall/maintenance mode. Source: https://sourceforge.net/projects/vjoystick/files/Beta%202.x/2.1.9.1-160719/ .
3. Configure one separate vJoy device per Wiimote, with X and Y axes and enough buttons for the table below. Confirm pointing and buttons in the vJoy monitor before starting RetroArch. Pointing must appear as X/Y (RetroArch axes 0/1), not Rx/Ry or Z/Rz.
4. Close RetroArch. Copy `autoconfig/dinput/vJoy Device.cfg` into RetroArch's configured Autoconfig directory under `dinput`. In RetroBat this is usually `<RetroBat>\emulators\retroarch\autoconfig\dinput`. Back up any existing profile with that name.
5. RetroArch Settings → Drivers: set **Input = dinput** and **Controller = dinput** (called Joypad in some versions), then save and fully restart RetroArch. The Controller/joypad driver is the important selector for this DirectInput autoconfig; changing Input alone while Controller stays xinput is insufficient. Other input backends may work, but both dinput settings are our documented test baseline. Select each Wiimote's actual vJoy device under Settings → Input → Port Controls. Device numbers can vary between computers.
6. For pointing ports use Analog to Digital Type **None**, Analog Sensitivity **1.0**, Analog Deadzone **0.0**. Under Settings → Input → Menu Controls enable **Disable Left Analog in Menu**. Otherwise Wiimote motion can move the menu selection continuously. Menu labels vary with RetroArch version.
7. Choose the core-specific Device Type under Quick Menu → Controls. Save a **Game Remap File** and, where appropriate, a Game Options File. Keep P1 mapped to port 1 and P2 to port 2 unless the current guide explicitly says otherwise. Internal hybrid routing eliminates duplicate vJoy bindings in the gun cores.

## Driver configuration reference

In the main RetroArch configuration these settings are:

```ini
input_driver = "dinput"
input_joypad_driver = "dinput"
```

These belong in RetroArch's configuration, not as an extra controller mapping. The `input_driver = "dinput"` field already in the autoconfig identifies its matching controller backend. Chihiro users playing with ordinary gamepads should select the driver appropriate to those pads instead.

Official driver guide: https://docs.libretro.com/guides/input-controller-drivers/ .

## Required button mapping

Match these assignments in Lichtknarre. vJoy configuration tools usually number buttons from 1; RetroArch's CFG numbers them from 0.

| Wiimote | vJoy button (1-based) | RetroArch CFG button | RetroPad |
|---|---:|---:|---|
| A | 1 | 0 | A |
| B | 2 | 1 | B |
| 1 | 3 | 2 | X |
| 2 | 4 | 3 | Y |
| Plus | 5 | 4 | Start |
| Minus | 6 | 5 | Select |
| Up | 8 | 7 | Up |
| Down | 9 | 8 | Down |
| Left | 10 | 9 | Left |
| Right | 11 | 10 | Right |

Home is intentionally unassigned in this profile; bind it to Menu Toggle manually if desired. The optional Plus+Minus→Escape AHK exit shortcut is not installed by this package. Avoid giving Escape/menu hotkeys conflicting actions without checking the result.

Core gun actions usually use **RetroPad buttons**, while native lightgun devices can use the extra gun bindings in this profile. Reload depends on the emulated gun and game. No personal GUIDs or device-index assignments are included.

If HIDHide is installed, allow the actual RetroArch executable to see vJoy; do not hide vJoy from it. If P2 follows P1, first check both Device Index assignments and old game remaps. Never bind both players to the same vJoy device for independent aiming.
