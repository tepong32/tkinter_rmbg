# Rembg Studio

A small Tkinter desktop app for removing image backgrounds in batches. It uses
[`rembg`](https://github.com/danielgatis/rembg) for local inference and Pillow
for image loading and output.

The window and application metadata currently report version **1.0.0**.

## Requirements

- Python 3.11, 3.12, or 3.13
- Tkinter (included with most standard Python installers; on Linux, install the
  system `python3-tk` package if needed)
- A CPU capable of running ONNX Runtime inference

The app uses the CPU version of ONNX Runtime. For a supported NVIDIA setup,
replace the `rembg[cpu]` extra in `requirements.txt` with the `rembg[gpu]` extra
and install the matching CUDA and cuDNN dependencies described in the rembg
documentation.

## Install and run

Create and activate a virtual environment, then install the dependencies and
launch the app:

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS or Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python remove_bg_with_python.py
```

For a repeatable Windows/Python 3.13 install, use
`python -m pip install -r requirements-lock-py313-win.txt` instead of the
general dependency resolver command above.

The Windows CPU package includes the U-2-Net model and works without internet
access. On first use, the app copies the model into the user's writable data
folder. Image processing runs in a background thread, so the window remains
responsive while a batch is running.

## Use

1. Add images individually or add a folder. Add more files to extend the list;
   use multi-select and **Remove selected** to edit the batch. Folder selection
   scans that folder only, not nested folders.
2. Choose an output preset and PNG or JPG. PNG retains transparency; JPG uses a
   white background where transparency was removed.
3. Start processing. PNG retains transparency; JPG composites the transparent
   area onto white.

Outputs are saved next to the source using `_removed` or `_bg_removed`, or with
a timestamp. The custom-folder preset saves each file there with `_output` in
its name. When an output name already exists, a numbered suffix is added to
avoid overwriting it. A final summary reports successful and failed files.

Supported inputs: PNG, JPG/JPEG, BMP, TIFF, and WebP.

See [third-party notices](THIRD_PARTY_NOTICES.md) for dependency and model
licensing information, and [the Windows packaging checklist](PACKAGING_CHECKLIST.md)
before creating a distributable build. Release documentation is versioned under
[`releases/`](releases/README.md); each backend/platform package carries its own
dependency lock and notices. The current Windows CPU package documentation is
marked as pending its first executable build. The default `u2net` model is about
176.3 MB and downloads on first use.
