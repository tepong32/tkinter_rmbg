🪄 Background Remover Utility (Python + Tkinter + rembg)

A lightweight desktop app built with Python, Tkinter, Pillow, and rembg that removes image backgrounds with just a few clicks — no code editing required.
Designed for both single-image cleanup and batch folder processing, perfect for quick media prep or production workflows.

---

✨ Features
🖼️ Core Functionality

Automatic Background Removal:
Powered by the rembg library for high-accuracy background detection and subject isolation.

Multi-Format Support:
Accepts .jpg, .jpeg, .png, and .webp images.

🧭 User Interface

File Explorer Integration:

Pick individual images or an entire folder via a native file dialog.

No more manual path editing in code.

Simple, Intuitive UI:
Minimal Tkinter interface with clear options for mode selection and format output.

🗂️ Batch Mode

Batch Folder Processing:
Select a folder, and the app automatically processes all supported images inside.

Output images are saved in a /processed subfolder within the same directory.

Great for bulk media cleanup or asset pipelines.

Automatic File Naming:
Each processed file keeps its original name with _rembg appended.

💾 Output Options

Save as PNG or JPG:
Choose between .png (preserves transparency) or .jpg (auto-converts transparent areas to white).

Smart Output Folder Handling:
Automatically creates a processed folder if it doesn’t exist.

⚙️ Error Handling

Graceful fallback when an image can’t be processed.

Prevents crashes from incompatible formats or read/write permission issues.

Clean console logs for easy debugging.

🔮 Future Enhancements (Planned)

Preview pane with before/after comparison.

Adjustable background removal intensity.

Drag-and-drop folder support.

Progress bar and success summary after batch operations.

Export presets (custom output naming templates, timestamp, or resolution options).

🧠 Usage
🪜 Step-by-Step Guide
🖼️ Single Image Mode

Launch the app.

Choose “Single Image” when prompted.

A file dialog will appear — select the image you want to process.

Select your output format (.png or .jpg).

The app removes the background and saves the output as:

⚠️ Common Issues

| Issue                            | Cause                                        | Fix                                                   |
| -------------------------------- | -------------------------------------------- | ----------------------------------------------------- |
| `cannot write mode RGBA as JPEG` | Image has transparency, but saving as `.jpg` | Automatically fixed in v3+ (auto-converts RGBA→RGB)   |
| Blank outputs                    | Non-image file or corrupted input            | Remove invalid files from the folder                  |
| No output files                  | Folder doesn’t contain supported image types | Ensure images are `.jpg`, `.jpeg`, `.png`, or `.webp` |
