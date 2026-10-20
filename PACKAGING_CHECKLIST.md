# Windows packaging checklist

## Build inputs

- Use Python 3.13 on Windows and install `requirements-lock-py313-win.txt` for a repeatable runtime dependency set.
- Build a one-folder bundle first. PyInstaller documents one-folder mode as its default; it is easier to inspect when ONNX Runtime DLLs or package data are missing.
- Include `assets/app_icon.ico`, `THIRD_PARTY_NOTICES.md`, and `LICENSES/` in the bundle.
- Use `assets/app_icon.ico` for the executable icon and `packaging/version_info.txt` for its Windows version resource. Keep both at `APP_VERSION` in `app_metadata.py`.
- Keep the bundle's model cache in the user's writable data directory. Do not put downloaded models beside the executable or in a temporary extraction directory.
- Create a separate, versioned output directory for every app version and backend variant. Start from `packaging/PACKAGE_README_TEMPLATE.md` and include the package-specific README, matching dependency lock, notices, license texts, and a SHA-256 file in every archive.
- Record the source commit, platform, backend, build date, executable name, and checksum in that version's README after the build. Never label a planned or unverified executable as tested.

## Model choice

The selected `u2net` model is about 176.3 MB (about 168 MiB) before packaging. The Windows CPU profile bundles it and copies it into the user's writable model cache on first use, so model initialization is offline. Keep the model checksum check and include the U-2-Net attribution and Apache-2.0 notice in every package.

## Release checks

- Build from a clean Windows virtual environment using the lock file.
- Launch the built app on a Windows machine without Python installed.
- Check first launch with internet disabled and with an existing model cache.
- Process PNG and JPG inputs, including uppercase extensions, and verify PNG transparency and JPG white compositing.
- Verify output naming, duplicate-name handling, failure reporting, bundled-model checksum errors, and model cache seeding.
- Inspect the built folder for the ONNX Runtime binaries, Tk runtime files, icon, notices, and license texts.
