# v1.0.0 verification — 2026-10-07

The maintainer reported testing all cores successfully before this packaging pass. The nine DLLs are byte-for-byte identical to the accepted RC2 binaries. Historical test logs are retained with their original labels; they are not new Windows test runs.

Packaging checks: ZIP integrity; readable source archives with safe relative member paths; core/info basename pairs; Windows AMD64 DLL headers; unique RetroBat system names; reference main config has 246 systems; recorded DLL and file SHA256 checksums. Full modified emulator source archives, patch history and component licenses are included. This is a mixed-license distribution: GPL components, Snes9x and FBNeo/Genesis noncommercial terms and other component licenses remain applicable. No blanket MIT license is applied to the emulator suite.

Build entry points and dependencies were inspected. The FBNeo mouse source archive already includes Makefile.mouse; the extra development copy is retained for reference. Chihiro source recovery previously passed git apply --check against its recorded base. Its Meson wrap sources and matching external library releases have now been included with download hashes and the pinned MXE recipes. Release sources can be rebuilt/modified, including replacement of static libraries; see development/BUILDING.md. No obfuscation, signing restriction or installer is imposed.

Scope: no clean Windows rebuild or binary-reproducibility comparison was run here. Toolchain image availability, exact environment reconstruction and all game/revision combinations are not certified. Do not describe these checks as a new gameplay test or universal compatibility guarantee. Public docs describe title-specific limitations. No commercial game ROMs, extracted commercial XBEs, Chihiro/Xbox BIOS or user saves are bundled.

An installer and automatic RetroBat configuration replacement are deferred. Retained upstream firmware/test source files in emulator checkouts follow their upstream licenses; “no BIOS bundled” in user setup means no required commercial Chihiro/Xbox firmware.

Packaging revision 2 separates full source from installation files. Complete modified core/converter code, dependency sources and build/test material are in the matching source asset. Core DLL and converter/runtime binaries are unchanged; archives and file hashes were checked. No fresh Windows rebuild or gameplay test was run during packaging.
