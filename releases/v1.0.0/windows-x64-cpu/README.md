# Rembg Studio 1.0.0 - Windows x64 - CPU

## Package details

- App version: `1.0.0`
- Package variant: `windows-x64-cpu`
- Archive: `RembgStudio-1.0.0-windows-x64-cpu.zip`
- Executable: `RembgStudio.exe` (run from the extracted package folder)
- Build profile: Python 3.13, Windows x64, CPU ONNX Runtime
- Build date: 2026-10-20
- Source revision: `76919240d06ec435c70159f2082ddc2b0b49e0b7` (working tree contained packaging changes)
- Executable SHA-256 is recorded in `SHA256SUMS.txt` alongside the archive.

## Install and use

Extract the complete ZIP to a writable folder, then run `RembgStudio.exe`. Add images or a folder, choose PNG or JPG and an output preset, then select **Remove backgrounds**. PNG preserves transparency. JPG fills transparent areas with white. The package includes the runtime, so Python does not need to be installed.

Keep the `_internal` folder beside the executable. It contains the bundled Python runtime, native libraries, model, and dependency files. The root of this extracted package also includes the dependency lock, notices, and license texts for convenient review.

## Offline model

This profile explicitly uses rembg's `u2net` model. The 175,997,641-byte model is bundled at `_internal/models/u2net/u2net.onnx`. On first run, the app verifies it and copies it to the user's writable app data folder. Inference then runs with the CPU ONNX Runtime and does not need internet access.

Bundled model SHA-256: `8d10d2f3bb75ae3b6d527c77944fc5e7dcd94b29809d47a739a7a728a912b491`.

## Dependencies and licenses

Direct Python dependencies are `rembg[cpu]==2.0.85`, `Pillow==12.3.0`, and `platformdirs==4.13.5`. The full Windows/Python 3.13 transitive lock is `requirements-lock-py313-win.txt`. Third-party and model notices are in `THIRD_PARTY_NOTICES.md`; corresponding license texts are in `LICENSES/` and `_internal/LICENSES/`.

## Known limitations

- Folder selection scans one folder level only.
- Image processing is CPU-based and may take time for large batches.
- This build targets Windows x64; it is not a portable build for macOS or Linux.

## Offline verification

The package was run with network proxy variables pointed at an unavailable local endpoint and an empty app cache. The bundled model was copied, checksum-verified, and loaded by ONNX Runtime's CPU provider.
