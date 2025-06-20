import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

class FileRenamerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📁 File Renamer GUI")
        self.root.geometry("500x400")

        # Folder selection
        self.folder_label = tk.Label(root, text="No folder selected", wraplength=400)
        self.folder_label.pack(pady=10)

        self.select_btn = tk.Button(root, text="Select Folder", command=self.select_folder)
        self.select_btn.pack(pady=5)

        # Prefix input
        self.prefix_label = tk.Label(root, text="Prefix:")
        self.prefix_label.pack()
        self.prefix_entry = tk.Entry(root)
        self.prefix_entry.insert(0, "file_")
        self.prefix_entry.pack(pady=5)

        # Start number input
        self.start_label = tk.Label(root, text="Start Number:")
        self.start_label.pack()
        self.start_entry = tk.Entry(root)
        self.start_entry.insert(0, "1")
        self.start_entry.pack(pady=5)

        # Extension filter
        self.ext_label = tk.Label(root, text="Filter by Extension (e.g. .jpg or .txt):")
        self.ext_label.pack()
        self.ext_entry = tk.Entry(root)
        self.ext_entry.pack(pady=5)

        # Rename button
        self.rename_btn = tk.Button(root, text="Rename Files", command=self.rename_files)
        self.rename_btn.pack(pady=20)

        # Folder path
        self.folder_path = ""

    def select_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.folder_path = path
            self.folder_label.config(text=f"Selected Folder:\n{path}")

    def rename_files(self):
        prefix = self.prefix_entry.get().strip() or "file_"
        try:
            start_number = int(self.start_entry.get().strip())
        except ValueError:
            messagebox.showerror("Invalid Input", "Start number must be an integer.")
            return

        ext_filter = self.ext_entry.get().strip().lower()
        if ext_filter and not ext_filter.startswith("."):
            ext_filter = "." + ext_filter

        if not self.folder_path:
            messagebox.showerror("No Folder", "Please select a folder first.")
            return

        files = os.listdir(self.folder_path)
        files = [f for f in files if os.path.isfile(os.path.join(self.folder_path, f))]

        if ext_filter:
            files = [f for f in files if f.lower().endswith(ext_filter)]

        if not files:
            messagebox.showinfo("No Files", "No files match your criteria.")
            return

        preview = "\n".join(
            f"{f} → {prefix}{i+start_number}{os.path.splitext(f)[1]}"
            for i, f in enumerate(files)
        )

        proceed = messagebox.askyesno("Confirm Rename", f"Preview:\n\n{preview}\n\nContinue?")
        if not proceed:
            return

        for i, f in enumerate(files):
            ext = os.path.splitext(f)[1]
            new_name = f"{prefix}{i+start_number}{ext}"
            os.rename(os.path.join(self.folder_path, f), os.path.join(self.folder_path, new_name))

        messagebox.showinfo("Done", "Files renamed successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileRenamerApp(root)
    root.mainloop()
