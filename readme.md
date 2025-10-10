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