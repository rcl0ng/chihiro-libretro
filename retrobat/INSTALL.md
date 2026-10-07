# Manual RetroBat registration

Close RetroBat and RetroArch and back up the files you edit. This release installs no launcher or driver and makes no automatic settings changes.

1. Copy the files from `cores` into `<RetroBat>\emulators\retroarch\cores`, and `info` into the configured Core Info directory (usually `emulators\retroarch\info`). Do not copy development archives into those folders.
2. Open **BatGui.exe → System List** and check the configuration file currently assigned to EACH system you want to use. An active per-system override can make an edit in `es_systems_main.cfg` appear ineffective.
3. The files normally live under `<RetroBat>\emulationstation\.emulationstation`. This folder may be hidden: enable Windows Explorer Hidden items or type the full path into the address bar.
4. Preferred manual route: edit the active file identified by BatGui. Find the `<system>` with the matching `<name>`, then its `<emulator name="libretro"><cores>` section. Add the lines below inside that `<cores>` element. Preserve other emulators, core entries, paths and extensions.
5. Optional reference files are supplied under `reference-configs`. Compare them with your active files before using any contents. BatGui identifies the active source file; this guide does not claim it can reassign that file. Edit the active file directly. The full es_systems_main.cfg reference contains 246 systems and both old and custom core choices. Per-system references contain only their named system. Compare with your installed RetroBat version before using them.
6. Save, restart RetroBat, then select **libretro** and the custom core in the game's advanced emulator settings. No changes to `es_settings.cfg` are needed merely to add core choices. RetroBat menu labels and handling vary by version; confirm the active file again if the core is absent.

The reference configurations derive from the maintainer’s tested installation, not a universal replacement for every RetroBat version. They contain no ROMs and do not choose the user's default core. Keep paths/extensions appropriate to your own installation. Upgrades can replace configuration files, so retain backups and these instructions.

| System `<name>` | Typical override file | Lines to add under libretro / cores |
|---|---|---|
| nes | es_systems_nes.cfg | `<core>fceumm_ir_gun</core>` |
| snes | es_systems_snes.cfg | `<core>snes9x_ir_gun</core>` and `<core>snes9x_analog_mouse</core>` |
| mastersystem / megadrive / megacd | Their active system file or es_systems_main.cfg | `<core>genesis_plus_gx_analog</core>` |
| psx | es_systems_psx.cfg | `<core>beetle_psx_ir_gun</core>` |
| saturn | es_systems_saturn.cfg | `<core>beetle_saturn_ir_gun</core>` |
| fbneo / mame | Their active system file or es_systems_main.cfg | `<core>fbneo_mouse</core>` and `<core>fbneo_shooter</core>` |
| chihiro (separate project) | es_systems_chihiro.cfg | `<core>chihiro</core>` |

Chihiro also needs `.bin` in its system's `<extension>` list. Keep BIOS in RetroArch's configured System/BIOS directory, not a path guessed from the install drive. Use Settings → Directory to confirm.

References: https://wiki.retrobat.org/advanced-features/batgui and https://wiki.retrobat.org/get-started/retrobat-folder-structure . Detailed per-system active-file behavior is also based on the maintainer’s working configuration and report; exact BatGui controls must be checked on the user's version.
