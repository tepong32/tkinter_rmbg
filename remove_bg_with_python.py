import os
import queue
import sys
import threading
from datetime import datetime
from pathlib import Path
from tkinter import (
    END,
    Listbox,
    StringVar,
    Tk,
    filedialog,
    messagebox,
)
from tkinter import ttk

from PIL import Image
from app_model import prepare_model
from app_metadata import APP_NAME, APP_VERSION, resource_path
from platformdirs import user_cache_path

cache_root = Path(os.environ.get("REMBG_STUDIO_CACHE_DIR") or
                  user_cache_path(APP_NAME, appauthor=APP_NAME))
cache_root.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("NUMBA_CACHE_DIR", str(cache_root / "numba"))
if getattr(sys, "frozen", False):
    # Numba cannot locate source files embedded in PyInstaller's archive.
    os.environ.setdefault("NUMBA_DISABLE_JIT", "1")

from rembg import new_session, remove


SUPPORTED_EXTENSIONS = (".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".webp")


class RembgApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{APP_NAME} v{APP_VERSION} - Batch Background Remover")
        self.root.geometry("700x720")
        self.root.minsize(620, 650)
        self.root.configure(bg="#f4f6fa")
        icon_path = resource_path("assets", "app_icon.ico")
        if icon_path.exists():
            self.root.iconbitmap(default=str(icon_path))

        style = ttk.Style(root)
        style.theme_use("clam")
        style.configure("App.TFrame", background="#f4f6fa")
        style.configure("Card.TFrame", background="#ffffff")
        style.configure("Title.TLabel", background="#f4f6fa", foreground="#172033",
                        font=("Segoe UI", 22, "bold"))
        style.configure("Subtitle.TLabel", background="#f4f6fa", foreground="#667085",
                        font=("Segoe UI", 10))
        style.configure("Section.TLabel", background="#ffffff", foreground="#172033",
                        font=("Segoe UI", 11, "bold"))
        style.configure("Muted.TLabel", background="#ffffff", foreground="#667085",
                        font=("Segoe UI", 9))
        style.configure("TButton", font=("Segoe UI", 10), padding=(12, 8))
        style.configure("Accent.TButton", background="#3157c8", foreground="#ffffff",
                        font=("Segoe UI", 10, "bold"), padding=(12, 10))
        style.map("Accent.TButton", background=[("active", "#2446ad"),
                                                  ("disabled", "#aeb9d5")])
        style.configure("TCombobox", padding=6, fieldbackground="#ffffff")
        style.configure("Horizontal.TProgressbar", troughcolor="#e7ebf3",
                         background="#3157c8", thickness=10)

        self.files = []
        self.worker_updates = queue.Queue()
        self.preset = StringVar(value="Same Folder (_removed)")
        self.output_format = StringVar(value=".png")
        self.presets = [
            "Same Folder (_removed)",
            "Same Folder (_bg_removed)",
            "Same Folder (with timestamp)",
            "Custom Folder (one output per file)",
        ]

        container = ttk.Frame(root, style="App.TFrame", padding=(26, 22))
        container.pack(fill="both", expand=True)
        ttk.Label(container, text=APP_NAME, style="Title.TLabel").pack(anchor="w")
        ttk.Label(container, text="Remove image backgrounds in batches.",
                  style="Subtitle.TLabel").pack(anchor="w", pady=(3, 18))

        files_card = ttk.Frame(container, style="Card.TFrame", padding=16)
        files_card.pack(fill="both", expand=True)
        files_header = ttk.Frame(files_card, style="Card.TFrame")
        files_header.pack(fill="x")
        ttk.Label(files_header, text="Images", style="Section.TLabel").pack(side="left")
        self.file_count_label = ttk.Label(files_header, text="No images selected",
                                          style="Muted.TLabel")
        self.file_count_label.pack(side="right")

        list_frame = ttk.Frame(files_card, style="Card.TFrame")
        list_frame.pack(fill="both", expand=True, pady=(12, 10))
        self.listbox = Listbox(
            list_frame, height=10, relief="flat", borderwidth=0,
            background="#f7f8fb", foreground="#26334d",
            selectbackground="#dce5ff", selectforeground="#172033",
            font=("Segoe UI", 10), activestyle="none", selectmode="extended",
        )
        self.listbox.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.configure(yscrollcommand=scrollbar.set)

        file_actions = ttk.Frame(files_card, style="Card.TFrame")
        file_actions.pack(fill="x")
        self.select_files_button = ttk.Button(
            file_actions, text="Add images", command=self.select_files
        )
        self.select_files_button.pack(side="left")
        self.select_folder_button = ttk.Button(
            file_actions, text="Add folder", command=self.select_folder
        )
        self.select_folder_button.pack(side="left", padx=(8, 0))
        self.clear_button = ttk.Button(file_actions, text="Clear list", command=self.clear_files)
        self.clear_button.pack(side="right")
        self.remove_button = ttk.Button(
            file_actions, text="Remove selected", command=self.remove_selected_files
        )
        self.remove_button.pack(side="right", padx=(0, 8))

        options_card = ttk.Frame(container, style="Card.TFrame", padding=16)
        options_card.pack(fill="x", pady=(14, 0))
        ttk.Label(options_card, text="Output settings", style="Section.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 10)
        )
        ttk.Label(options_card, text="Save location", style="Muted.TLabel").grid(
            row=1, column=0, sticky="w", padx=(0, 14), pady=4
        )
        self.preset_menu = ttk.Combobox(
            options_card, textvariable=self.preset, values=self.presets,
            state="readonly", width=38,
        )
        self.preset_menu.grid(row=1, column=1, sticky="ew", pady=4)
        ttk.Label(options_card, text="File format", style="Muted.TLabel").grid(
            row=2, column=0, sticky="w", padx=(0, 14), pady=4
        )
        self.format_menu = ttk.Combobox(
            options_card, textvariable=self.output_format,
            values=(".png", ".jpg"), state="readonly", width=12,
        )
        self.format_menu.grid(row=2, column=1, sticky="w", pady=4)
        options_card.columnconfigure(1, weight=1)
        self.format_hint = ttk.Label(
            options_card, text="PNG keeps transparency.", style="Muted.TLabel"
        )
        self.format_hint.grid(row=3, column=1, sticky="w", pady=(3, 0))
        self.output_format.trace_add("write", self._update_format_hint)

        self.process_button = ttk.Button(
            container, text="Remove backgrounds", command=self.process_files,
            style="Accent.TButton",
        )
        self.process_button.pack(fill="x", pady=(14, 12))

        progress_card = ttk.Frame(container, style="Card.TFrame", padding=16)
        progress_card.pack(fill="x")
        progress_header = ttk.Frame(progress_card, style="Card.TFrame")
        progress_header.pack(fill="x", pady=(0, 8))
        ttk.Label(progress_header, text="Batch progress", style="Section.TLabel").pack(side="left")
        self.progress_count_label = ttk.Label(progress_header, text="0 / 0",
                                              style="Muted.TLabel")
        self.progress_count_label.pack(side="right")
        self.progress = ttk.Progressbar(progress_card, mode="determinate")
        self.progress.pack(fill="x")
        self.status_label = ttk.Label(progress_card, text="Ready", style="Muted.TLabel")
        self.status_label.pack(anchor="w", pady=(9, 0))
        self.root.after(100, self._poll_worker_updates)

    def select_files(self):
        paths = filedialog.askopenfilenames(
            title="Select Image Files",
            filetypes=[
                ("Image files", tuple(
                    pattern
                    for extension in SUPPORTED_EXTENSIONS
                    for pattern in (f"*{extension}", f"*{extension.upper()}")
                )),
                ("All files", "*.*"),
            ],
        )
        self._load_files(paths)

    def select_folder(self):
        folder = filedialog.askdirectory(title="Select Folder Containing Images")
        if not folder:
            return

        try:
            paths = [
                os.path.join(folder, name)
                for name in os.listdir(folder)
                if name.lower().endswith(SUPPORTED_EXTENSIONS)
                and os.path.isfile(os.path.join(folder, name))
            ]
        except OSError as error:
            messagebox.showerror("Unable to Read Folder", str(error))
            return

        if not paths:
            messagebox.showinfo("No Images", "No supported image files found in that folder.")
            return

        self._load_files(paths)

    def _load_files(self, paths):
        if not paths:
            return
        self.files = sorted(dict.fromkeys([*self.files, *paths]))
        self._refresh_file_list()
        self.status_label.config(text="Ready")

    def _refresh_file_list(self):
        self.listbox.delete(0, END)
        basenames = [os.path.basename(path) for path in self.files]
        for path in self.files:
            basename = os.path.basename(path)
            display_name = basename
            if basenames.count(basename) > 1:
                display_name = f"{basename}  —  {os.path.dirname(path)}"
            self.listbox.insert(END, display_name)
        count = len(self.files)
        self.file_count_label.config(
            text="No images selected" if count == 0 else f"{count} image(s) in batch"
        )

    def remove_selected_files(self):
        selected = set(self.listbox.curselection())
        if not selected:
            return
        self.files = [path for index, path in enumerate(self.files) if index not in selected]
        self._refresh_file_list()

    def clear_files(self):
        self.files.clear()
        self._refresh_file_list()
        self.status_label.config(text="Ready")

    def _update_format_hint(self, *_):
        if self.output_format.get() == ".jpg":
            self.format_hint.config(text="JPG uses a white background where transparency was removed.")
        else:
            self.format_hint.config(text="PNG keeps the transparent background.")

    def process_files(self):
        if not self.files:
            messagebox.showwarning("No Files", "Please select at least one image or folder.")
            return

        custom_output_dir = None
        if self.preset.get() == "Custom Folder (one output per file)":
            custom_output_dir = filedialog.askdirectory(title="Select Output Folder")
            if not custom_output_dir:
                return

        job = {
            "files": list(self.files),
            "preset": self.preset.get(),
            "format": self.output_format.get(),
            "custom_output_dir": custom_output_dir,
        }
        self.progress["value"] = 0
        self.progress["maximum"] = len(job["files"])
        self.progress_count_label.config(text=f"0 / {len(job['files'])}")
        self.status_label.config(text="Preparing the bundled model and runtime…")
        self._set_busy(True)

        threading.Thread(target=self._process_files_worker, args=(job,), daemon=True).start()

    def _process_files_worker(self, job):
        files = job["files"]
        successes = []
        failures = []

        try:
            prepare_model()
            session = new_session("u2net")
        except Exception as error:
            failures = [(path, str(error)) for path in files]
            self.worker_updates.put(("finished", successes, failures))
            return

        for index, input_path in enumerate(files, start=1):
            try:
                output_path = self._output_path(input_path, job)
                with Image.open(input_path) as source:
                    output = remove(source.convert("RGBA"), session=session)

                output = output.convert("RGBA")
                if job["format"] == ".jpg":
                    rgb_output = Image.new("RGB", output.size, "white")
                    rgb_output.paste(output, mask=output.getchannel("A"))
                    rgb_output.save(output_path, "JPEG", quality=95)
                else:
                    output.save(output_path, "PNG")
                successes.append((input_path, output_path))
            except Exception as error:
                failures.append((input_path, str(error)))

            self.worker_updates.put(("progress", index, len(files), input_path))

        self.worker_updates.put(("finished", successes, failures))

    def _poll_worker_updates(self):
        try:
            while True:
                update = self.worker_updates.get_nowait()
                if update[0] == "progress":
                    self._update_progress(*update[1:])
                else:
                    self._finish_processing(*update[1:])
        except queue.Empty:
            pass
        self.root.after(100, self._poll_worker_updates)

    @staticmethod
    def _output_path(input_path, job):
        source = Path(input_path)
        output_format = job["format"]
        preset = job["preset"]

        if preset == "Same Folder (_removed)":
            directory = source.parent
            stem = f"{source.stem}_removed"
        elif preset == "Same Folder (_bg_removed)":
            directory = source.parent
            stem = f"{source.stem}_bg_removed"
        elif preset == "Same Folder (with timestamp)":
            directory = source.parent
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            stem = f"{source.stem}_{timestamp}"
        else:
            directory = Path(job["custom_output_dir"])
            stem = f"{source.stem}_output"

        candidate = directory / f"{stem}{output_format}"
        suffix = 1
        while candidate.exists() or candidate.resolve() == source.resolve():
            candidate = directory / f"{stem}_{suffix}{output_format}"
            suffix += 1
        return str(candidate)

    def _update_progress(self, index, total, input_path):
        self.progress["value"] = index
        self.progress_count_label.config(text=f"{index} / {total}")
        self.status_label.config(
            text=f"Processed {index}/{total}: {os.path.basename(input_path)}"
        )

    def _finish_processing(self, successes, failures):
        self._set_busy(False)
        total = len(successes) + len(failures)
        self.progress["value"] = total
        self.progress_count_label.config(text=f"{total} / {total}")

        if failures:
            self.status_label.config(text=f"Finished with {len(failures)} failure(s).")
            details = "\n".join(
                f"{os.path.basename(path)}: {error}" for path, error in failures[:8]
            )
            if len(failures) > 8:
                details += f"\n…and {len(failures) - 8} more failure(s)."
            messagebox.showwarning(
                "Processing Finished",
                f"{len(successes)} of {total} file(s) processed successfully.\n\n"
                f"Failures:\n{details}",
            )
        else:
            self.status_label.config(text=f"Finished: {total} image(s) processed successfully.")
            messagebox.showinfo("Done", f"Background removal completed for {total} file(s).")

    def _set_busy(self, busy):
        state = "disabled" if busy else "normal"
        for widget in (
            self.select_files_button,
            self.select_folder_button,
            self.remove_button,
            self.clear_button,
            self.process_button,
            self.preset_menu,
            self.format_menu,
        ):
            widget.config(state=state)


if __name__ == "__main__":
    if "--verify-offline" in sys.argv:
        try:
            prepare_model()
            verified_session = new_session("u2net")
            if "CPUExecutionProvider" not in verified_session.inner_session.get_providers():
                raise RuntimeError("ONNX Runtime did not activate its CPU provider.")
        except Exception:
            raise SystemExit(1)
        raise SystemExit(0)

    root = Tk()
    app = RembgApp(root)
    root.mainloop()
