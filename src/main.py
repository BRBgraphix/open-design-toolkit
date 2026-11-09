"""Tkinter desktop interface for Open Design Toolkit."""
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from src.image_optimizer import optimize_folder
from src.batch_rename import build_rename_plan, apply_rename_plan


class OpenDesignToolkit(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Open Design Toolkit")
        self.geometry("760x560")
        self.minsize(650, 480)
        self.configure(padx=18, pady=18)

        ttk.Label(self, text="Open Design Toolkit", font=("Segoe UI", 20, "bold")).pack(anchor="w")
        ttk.Label(
            self,
            text="Free tools for organizing and preparing design assets.",
        ).pack(anchor="w", pady=(0, 16))

        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill="both", expand=True)

        self._build_optimizer_tab()
        self._build_renamer_tab()

        self.status = tk.StringVar(value="Ready")
        ttk.Label(self, textvariable=self.status, relief="sunken", anchor="w").pack(fill="x", pady=(12, 0))

    def _folder_row(self, parent, label, variable, command):
        row = ttk.Frame(parent)
        row.pack(fill="x", pady=7)
        ttk.Label(row, text=label, width=17).pack(side="left")
        ttk.Entry(row, textvariable=variable).pack(side="left", fill="x", expand=True, padx=6)
        ttk.Button(row, text="Browse…", command=command).pack(side="left")

    def _build_optimizer_tab(self):
        tab = ttk.Frame(self.tabs, padding=16)
        self.tabs.add(tab, text="Image Optimizer")
        self.image_source = tk.StringVar()
        self.image_output = tk.StringVar()
        self.jpeg_quality = tk.IntVar(value=85)

        ttk.Label(tab, text="Optimize PNG and JPEG images in bulk.", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 12))
        self._folder_row(tab, "Source folder", self.image_source, self._choose_image_source)
        self._folder_row(tab, "Output folder", self.image_output, self._choose_image_output)

        quality_row = ttk.Frame(tab)
        quality_row.pack(fill="x", pady=12)
        ttk.Label(quality_row, text="JPEG quality", width=17).pack(side="left")
        ttk.Scale(quality_row, from_=40, to=95, variable=self.jpeg_quality, orient="horizontal").pack(side="left", fill="x", expand=True)
        self.quality_label = ttk.Label(quality_row, text="85")
        self.quality_label.pack(side="left", padx=8)
        self.jpeg_quality.trace_add("write", lambda *_: self.quality_label.config(text=str(self.jpeg_quality.get())))

        ttk.Label(tab, text="Original images are not changed. Results are saved in the output folder.", wraplength=650).pack(anchor="w", pady=8)
        ttk.Button(tab, text="Optimize images", command=self._run_optimizer).pack(anchor="w", pady=8)

    def _build_renamer_tab(self):
        tab = ttk.Frame(self.tabs, padding=16)
        self.tabs.add(tab, text="Batch Renamer")
        self.rename_folder = tk.StringVar()
        self.prefix = tk.StringVar(value="design_")
        self.start_number = tk.IntVar(value=1)
        self.rename_plan = []

        ttk.Label(tab, text="Rename files in one folder with a numbered sequence.", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 12))
        self._folder_row(tab, "Folder", self.rename_folder, self._choose_rename_folder)

        fields = ttk.Frame(tab)
        fields.pack(fill="x", pady=8)
        ttk.Label(fields, text="Filename prefix").pack(side="left")
        ttk.Entry(fields, textvariable=self.prefix, width=20).pack(side="left", padx=6)
        ttk.Label(fields, text="Start number").pack(side="left", padx=(12, 0))
        ttk.Spinbox(fields, from_=0, to=999999, textvariable=self.start_number, width=8).pack(side="left", padx=6)

        ttk.Button(tab, text="Preview rename", command=self._preview_rename).pack(anchor="w", pady=8)
        self.preview = tk.Text(tab, height=12, wrap="none", state="disabled")
        self.preview.pack(fill="both", expand=True, pady=6)
        ttk.Button(tab, text="Apply rename", command=self._apply_rename).pack(anchor="w", pady=8)

    def _choose_image_source(self):
        folder = filedialog.askdirectory()
        if folder:
            self.image_source.set(folder)
            if not self.image_output.get():
                self.image_output.set(str(Path(folder) / "optimized"))

    def _choose_image_output(self):
        folder = filedialog.askdirectory()
        if folder:
            self.image_output.set(folder)

    def _choose_rename_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.rename_folder.set(folder)

    def _run_optimizer(self):
        if not self.image_source.get() or not self.image_output.get():
            messagebox.showwarning("Choose folders", "Select both source and output folders first.")
            return
        try:
            results = optimize_folder(
                Path(self.image_source.get()),
                Path(self.image_output.get()),
                int(self.jpeg_quality.get()),
            )
            self.status.set(f"Optimized {len(results)} image(s).")
            messagebox.showinfo("Optimization complete", f"Created {len(results)} optimized image(s).")
        except Exception as exc:
            messagebox.showerror("Optimization failed", str(exc))

    def _preview_rename(self):
        try:
            self.rename_plan = build_rename_plan(
                Path(self.rename_folder.get()),
                self.prefix.get(),
                int(self.start_number.get()),
            )
            lines = [f"{src.name}  →  {dst.name}" for src, dst in self.rename_plan]
            self.preview.configure(state="normal")
            self.preview.delete("1.0", "end")
            self.preview.insert("1.0", "\n".join(lines) if lines else "No files need renaming.")
            self.preview.configure(state="disabled")
            self.status.set(f"Preview ready: {len(self.rename_plan)} file(s).")
        except Exception as exc:
            messagebox.showerror("Cannot create preview", str(exc))

    def _apply_rename(self):
        if not self.rename_plan:
            messagebox.showwarning("No preview", "Create and review a rename preview first.")
            return
        if not messagebox.askyesno("Confirm rename", f"Rename {len(self.rename_plan)} file(s)? Make sure you have a backup."):
            return
        try:
            renamed = apply_rename_plan(self.rename_plan)
            self.rename_plan = []
            self.status.set(f"Renamed {len(renamed)} file(s).")
            messagebox.showinfo("Rename complete", f"Renamed {len(renamed)} file(s).")
            self._preview_rename()
        except Exception as exc:
            messagebox.showerror("Rename failed", str(exc))


def main():
    app = OpenDesignToolkit()
    app.mainloop()


if __name__ == "__main__":
    main()
