import os
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime

class FileRenamerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📁 File Renamer GUI")
        self.root.geometry("500x420")

        self.folder_label = tk.Label(root, text="No folder selected", wraplength=450)
        self.folder_label.pack(pady=10)

        self.select_btn = tk.Button(root, text="Select Folder", command=self.select_folder)
        self.select_btn.pack()

        self.prefix_label = tk.Label(root, text="Prefix:")
        self.prefix_label.pack()
        self.prefix_entry = tk.Entry(root)
        self.prefix_entry.insert(0, "file_")
        self.prefix_entry.pack()

        self.start_label = tk.Label(root, text="Start Number:")
        self.start_label.pack()
        self.start_entry = tk.Entry(root)
        self.start_entry.insert(0, "1")
        self.start_entry.pack()

        self.ext_label = tk.Label(root, text="Extension Filter (e.g. .jpg or .txt):")
        self.ext_label.pack()
        self.ext_entry = tk.Entry(root)
        self.ext_entry.pack()

        self.rename_btn = tk.Button(root, text="Rename Files", command=self.rename_files)
        self.rename_btn.pack(pady=10)

        self.undo_btn = tk.Button(root, text="Undo Last Rename", command=self.undo_rename)
        self.undo_btn.pack()

        self.folder_path = ""
        self.last_renamed = []

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
            messagebox.showerror("No Folder", "Please select a folder.")
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

        if not messagebox.askyesno("Confirm Rename", f"Preview:\n\n{preview}\n\nContinue?"):
            return

        self.last_renamed = []  # Reset previous log

        log_path = os.path.join(self.folder_path, "rename_log.txt")
        with open(log_path, "a", encoding="utf-8") as log:
            log.write(f"\n=== Rename Operation @ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")

            for i, f in enumerate(files):
                ext = os.path.splitext(f)[1]
                new_name = f"{prefix}{i+start_number}{ext}"
                old_path = os.path.join(self.folder_path, f)
                new_path = os.path.join(self.folder_path, new_name)

                os.rename(old_path, new_path)
                self.last_renamed.append((new_name, f))  # Save for undo (reversed)

                log.write(f"{f} → {new_name}\n")

        messagebox.showinfo("Success", "Files renamed successfully.\nLog saved.")

    def undo_rename(self):
        if not self.last_renamed:
            messagebox.showwarning("Nothing to Undo", "No previous renaming found.")
            return

        try:
            for new_name, original_name in self.last_renamed:
                new_path = os.path.join(self.folder_path, new_name)
                original_path = os.path.join(self.folder_path, original_name)
                if os.path.exists(new_path):
                    os.rename(new_path, original_path)
            messagebox.showinfo("Undo Complete", "Last renaming operation has been undone.")
            self.last_renamed = []
        except Exception as e:
            messagebox.showerror("Undo Failed", f"An error occurred:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileRenamerApp(root)
    root.mainloop()
