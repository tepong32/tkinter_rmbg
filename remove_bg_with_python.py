import os
from datetime import datetime
from tkinter import (
    Tk, Button, Label, Listbox, filedialog, StringVar, OptionMenu, END, messagebox
)
from tkinter import ttk
from rembg import remove
from PIL import Image

class RembgApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rembg Utility - Background Remover")
        self.root.geometry("520x520")
        self.root.resizable(False, False)

        # --- UI State ---
        self.files = []
        self.preset = StringVar(value="Same Folder (_removed)")
        self.output_format = StringVar(value=".png")
        self.presets = [
            "Same Folder (_removed)",
            "Same Folder (_bg_removed)",
            "Same Folder (with timestamp)",
            "Custom Folder (rembg_output.png per file)"
        ]

        # --- UI Layout ---
        Label(root, text="Selected Images:", font=("Arial", 12, "bold")).pack(pady=(10, 5))
        self.listbox = Listbox(root, width=60, height=10)
        self.listbox.pack(pady=(0, 10))

        Button(root, text="Select Images", command=self.select_files, width=20, bg="#4CAF50", fg="white").pack(pady=5)

        Label(root, text="Output Preset:", font=("Arial", 11)).pack(pady=(15, 5))
        OptionMenu(root, self.preset, *self.presets).pack()

        Label(root, text="Output Format:", font=("Arial", 11)).pack(pady=(15, 5))
        OptionMenu(root, self.output_format, ".png", ".jpg").pack()

        Button(root, text="Start Removing Background", command=self.process_files, width=30, bg="#2196F3", fg="white").pack(pady=(20, 10))

        # Progress bar
        self.progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=(5, 5))

        self.status_label = Label(root, text="", fg="gray")
        self.status_label.pack(pady=(5, 0))

    # --- Select Files ---
    def select_files(self):
        paths = filedialog.askopenfilenames(
            title="Select Image Files",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff;*.webp")]
        )
        if paths:
            self.files = paths
            self.listbox.delete(0, END)
            for f in self.files:
                self.listbox.insert(END, os.path.basename(f))
            self.status_label.config(text=f"{len(self.files)} file(s) selected.")

    # --- Process Files ---
    def process_files(self):
        if not self.files:
            messagebox.showwarning("No Files", "Please select at least one image file.")
            return

        preset = self.preset.get()
        chosen_format = self.output_format.get()
        total_files = len(self.files)
        custom_output_dir = None

        # Ask once for custom folder if needed
        if preset == "Custom Folder (rembg_output.png per file)":
            custom_output_dir = filedialog.askdirectory(title="Select Output Folder")
            if not custom_output_dir:
                messagebox.showinfo("Cancelled", "Output folder selection cancelled.")
                return

        # Initialize progress bar
        self.progress["value"] = 0
        self.progress["maximum"] = total_files
        self.status_label.config(text="Processing...", fg="orange")
        self.root.update_idletasks()

        for idx, input_path in enumerate(self.files, start=1):
            try:
                base, ext = os.path.splitext(input_path)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                # --- Determine output path ---
                if preset == "Same Folder (_removed)":
                    output_path = f"{base}_removed{chosen_format}"
                elif preset == "Same Folder (_bg_removed)":
                    output_path = f"{base}_bg_removed{chosen_format}"
                elif preset == "Same Folder (with timestamp)":
                    output_path = f"{base}_{timestamp}{chosen_format}"
                else:  # Custom folder
                    filename = f"{os.path.splitext(os.path.basename(input_path))[0]}_output{chosen_format}"
                    output_path = os.path.join(custom_output_dir, filename)

                # --- Process image ---
                inp = Image.open(input_path)
                output = remove(inp)

                # Convert RGBA → RGB if JPEG (no alpha)
                if chosen_format.lower() in [".jpg", ".jpeg"]:
                    bg = Image.new("RGB", output.size, (255, 255, 255))
                    bg.paste(output, mask=output.split()[3])
                    bg.save(output_path, "JPEG")
                else:
                    output.save(output_path)

                self.progress["value"] = idx
                self.status_label.config(text=f"Processed {idx}/{total_files}: {os.path.basename(input_path)}")
                self.root.update_idletasks()

            except Exception as e:
                messagebox.showerror("Error", f"Failed to process {os.path.basename(input_path)}\n\n{e}")

        self.status_label.config(text=f"✅ All done! {total_files} file(s) processed.", fg="green")
        messagebox.showinfo("Done", "Background removal completed!")

# --- Run the App ---
if __name__ == "__main__":
    root = Tk()
    app = RembgApp(root)
    root.mainloop()
