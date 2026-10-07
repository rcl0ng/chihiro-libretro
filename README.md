# Sega - Chihiro — v1.0.0

Windows x64 Chihiro libretro core plus ChihiroPack package-to-BIN converter. This is an independent community project built on Tovarichtch/xemu and danprice142/xemu-libretro. Maintainer testing established nine games playable; widescreen gun games were calibrated successfully and final load/exit checks had no hiccups. Coverage is specific to tested revisions, not every Chihiro dump.

## Downloads

- **[Windows x64 core + converter](https://github.com/rcl0ng/chihiro-libretro/releases/download/v1.0.0/Chihiro_Libretro_v1.0.0_Windows_x64.zip)** — installation files, converter runtime, guides, info/autoconfig and license notices.
- **[Full modified source](https://github.com/rcl0ng/chihiro-libretro/releases/download/v1.0.0/Chihiro_Libretro_v1.0.0_Source.zip)** — extracted modified Chihiro core, converter code, patches, build/test records, pinned dependency sources and notices.
- **[SHA256 checksums](https://github.com/rcl0ng/chihiro-libretro/releases/download/v1.0.0/Chihiro_Libretro_v1.0.0_SHA256SUMS.txt)** — verify both downloads.
- [Release page](https://github.com/rcl0ng/chihiro-libretro/releases/tag/v1.0.0)

GitHub's automatic Source code ZIP/tar.gz contains this smaller repository tree. Use Full modified source above for the complete emulator code. Keep the matching source and Windows assets available together.

**Vulkan is strongly recommended. Use a fresh RetroArch process for each game.**

## Install and convert

**Start with [INSTALL-RETROARCH.md](INSTALL-RETROARCH.md). Standalone RetroArch is the primary setup; RetroBat integration is entirely optional.**

Copy `cores/chihiro_libretro.dll` and `info/chihiro_libretro.info` into RetroArch's configured Core and Core Info directories. Keep filename/core ID `chihiro`. For RetroBat use `retrobat/INSTALL.md`. The converter is in `converter/ChihiroPack`: keep its EXE, Python files, runtime and 7za.exe together. Put complete game folders/ZIPs/7z packages in its `input` directory and double-click `Convert_All_Packages.bat`; BINs and verification reports appear in `output`. Single-package drag/drop also works. Read its README for required boot.id/XBE package structure and size limits. It does not decrypt dumps or convert CHD/GD-ROM images directly.

Use `docs/CHIHIRO-SETUP.md` for BIOS, controls, cards, calibration and widescreen. Chihiro supports normal gamepad/XInput configurations for non-gun games and **Wiimotes through Lichtknarre/vJoy** for gun games. The shared vJoy autoconfig and mapping guide are included as an optional setup; vJoy is not required for ordinary gamepad use.

## Tested game scope

| Game | Main controls/features |
|---|---|
| Virtua Cop 3 | Two guns, calibration, optional widescreen |
| The House of the Dead 3 | Two guns, A pump/reload, optional widescreen |
| Ghost Squad | Two guns, card insertion, optional widescreen |
| OutRun 2 | Gamepad driving, optional widescreen |
| OutRun 2 Special Tours | Gamepad driving; additional firmware; optional widescreen |
| Maximum Tune 1 Export | Calibrated steering, persistent card, optional widescreen |
| Maximum Tune 2 Export | Calibrated steering, separate persistent card, optional widescreen |
| Crazy Taxi High Roller | Gamepad driving, optional widescreen |
| Ollie King | Gamepad board/foot/grab controls, optional widescreen |

Sega Golf 2006 is not recommended/established as playable. Menu art can stretch and HUD elements can remain at 4:3 positions. Widescreen patches require recognized executable signatures and change emulated memory only; BIN files remain untouched. **Use one game per RetroArch process**; quit and relaunch before another title. Public release version is 1.0.0, with the original tested v15 binary retained unchanged.

## Source, licensing and verification

The full source ZIP contains the modified emulator tree under `source/chihiro/chihiro-source/`, the converter under `converter/ChihiroPack/source/`, and patches/build/test records under `development/chihiro/source/`. External library sources and pinned MXE recipes are in `development/chihiro/dependencies/`. These paths refer to the downloaded source ZIP. This repository contains the public docs, configuration, converter code and selected build/patch records.

QEMU/xemu and individual dependencies retain their upstream terms. The converter code is MIT; its Python and 7-Zip dependencies have separate terms. Do not apply a blanket license to the combined project. Commercial games, extracted game executables, Chihiro/Xbox BIOS and user saves are not supplied.

Core/converter binaries are unchanged from the accepted build. Source/archive/hash checks passed; no fresh Windows rebuild or universal compatibility guarantee is claimed. See `docs/RELEASE-VERIFICATION.md` for scope. Historical developer notes retain their original development labels and do not supersede current setup guides.
