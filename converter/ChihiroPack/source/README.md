# ChihiroPack 1.0 — Windows x64

Create a 496 MiB FATX BIN from a complete Chihiro XBE package. This packages the existing files without modifying game code. No game files or BIOS are included.

## Click-to-run batch conversion

1. Extract the entire ZIP to a writable folder. Keep ChihiroPack.exe, chihiro_pack.py, runtime and 7za.exe together.
2. Put each game folder, ZIP or 7z package directly inside `input`. One complete game per item; do not put the BIN output there.
3. Double-click `Convert_All_Packages.bat`.
4. Find BINs and adjacent `.verification.json` reports in `output`. Read `batch-conversion.log` if anything fails.

The batch continues after a failed package. Existing BINs and reports are preserved; move successful inputs out of `input` before rerunning, or choose a fresh output directory. Each BIN needs about 496 MiB free space, plus temporary extracted files for archives.

For a single package, drag its folder, ZIP or 7z onto ChihiroPack.exe. The BIN and report are created beside that package. Double-click the EXE to enter a path interactively. Python and archive tools are bundled; no separate installation is required.

## Command line

```bat
ChihiroPack.exe create "D:\Packages\OutRun2.game.7z" -o "D:\Games\OutRun2.bin"
ChihiroPack.exe create "D:\Packages" --batch --output-dir "D:\Games"
ChihiroPack.exe verify "D:\Games\OutRun2.bin"
```

A complete package must contain a valid 480-byte BTID/XBAM `boot.id`, its referenced XBE and all game assets. Nested packaging folders are handled automatically. The tool rejects missing executables, multiple game roots, unsupported FATX names, unsafe archive paths, links and oversized images. It does not invent boot metadata, decrypt dumps, or convert CHD/GD-ROM formats. For those formats see [Chihiro-netboot](https://github.com/Tovarichtch/chihiro-netboot).

Each conversion checks the image using an independent FAT-chain/directory reader and compares every file size and SHA-256 with the original package. Reports also record the whole image SHA-256. Keep the report beside its BIN for a later full comparison. Verification without a report checks filesystem structure only.

## Games and emulation

Maximum Tune 1/2 packages supplied for this build passed all 1,298 / 2,272 file comparisons. OutRun 2, OutRun 2 Special Tours and Sega Golf 2006 packages can be attempted with the same tool, provided they meet the requirements and fit. Conversion success does not establish game playability. OutRun 2 Special Tours needs the native fork's network firmware; Sega Golf controls/playability are not yet confirmed in our core.

Windows launcher and BAT execution require user testing on Windows. Conversion, archive extraction, native FATX geometry, payload hashing, corruption detection, overwrite protection and batch continuation were exercised on Linux using the same Python implementation. No ROMs were patched.

## Source and reproducible packaging

`source` contains the MIT-licensed converter, Unicode Windows launcher, CMake build, tests, release script and a GitHub Actions workflow. Place that directory's contents at the root of a dedicated repository to use the workflow; it has not been run on GitHub yet.

Windows: `cmake -S . -B build -A x64`, `cmake --build build --config Release`, copy `build\Release\ChihiroPack.exe` to the project root, then `python prepare_release.py`. The release script downloads pinned official Python and 7-Zip dependencies and checks their SHA-256 values. Python 3.11+ is needed for developer scripts. Run `python test_converter.py` with 7-Zip on PATH. Linux users can run `python3 chihiro_pack.py` directly (install 7zz/7z for archives).

Python and 7-Zip keep their own licenses under `licenses` and `runtime`. The corresponding 7-Zip source archive is under `third_party/7zip`; download URLs and hashes are in `dependency-checksums.json`. No upstream emulator code is included in this converter.
