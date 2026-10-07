# Full source and component notices

[Full modified source](https://github.com/rcl0ng/chihiro-libretro/releases/download/v1.0.0/Chihiro_Libretro_v1.0.0_Source.zip) · [Windows core + converter](https://github.com/rcl0ng/chihiro-libretro/releases/download/v1.0.0/Chihiro_Libretro_v1.0.0_Windows_x64.zip) · [Checksums](https://github.com/rcl0ng/chihiro-libretro/releases/download/v1.0.0/Chihiro_Libretro_v1.0.0_SHA256SUMS.txt)

The source asset contains:

- `source/chihiro/chihiro-source/`: recovered modified emulator tree, upstream notices, Meson wrap pins/packagefiles and build entry points.
- `development/chihiro/source/`: combined patch against the recorded upstream commit, exact original build flags, test scripts and historical results.
- `development/chihiro/dependencies/`: library source releases, Meson overlay archives, download hashes and pinned MXE source/build recipes.
- `converter/ChihiroPack/source/`: launcher C source, Python converter, batch script, CMake/build workflow and tests.
- `converter/ChihiroPack/third_party/7zip/`: source matching the bundled 7-Zip version.
- `licenses/` and converter dependency notices: preserved component terms. Notices inside source trees also remain applicable.

GitHub's automatic Source code download contains the smaller repository tree. Keep the full source asset published with the Windows build. No fresh Windows rebuild was performed; the retained build records and dependency pins document the accepted build without claiming reproducible DLL hashes. See development/chihiro/source/BUILD.txt for the original command and toolchain. Extract dependency archives as needed; retain Meson wrap/packagefile overlays. Compiler/toolchain executables are not supplied.
