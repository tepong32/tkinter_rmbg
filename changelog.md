🧾 Changelog
v3.0 — Batch Folder Mode Release (2025-10-10)
🆕 New

Added batch folder selection and auto-creation of /processed output folder.

Added output format chooser (.png / .jpg).

Implemented smart file naming with _rembg suffix.

⚙️ Improvements

Handles transparent-to-RGB conversion automatically.

Streamlined user prompts for smoother UX.

Added internal checks for invalid or corrupted files.

🐞 Fixes

Fixed crash for “cannot write mode RGBA as JPEG”.

Improved stability during large batch operations.

v2.0 — File Explorer Integration

Introduced Tkinter file dialog for selecting input/output paths.

Removed hardcoded paths from the script.

Added basic error handling for missing files.

v1.0 — Initial CLI Version

Command-line implementation using rembg and Pillow.

Single image processing with fixed input/output paths.