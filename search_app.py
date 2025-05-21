import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import io
from db_handler import DBHandler
from tkinter import filedialog
import os
class SearchApp:
    def __init__(self, parent):
        self.parent = parent
        self.db = DBHandler()

        # Input field for work order
        self.label = tk.Label(parent, text="Enter Work Order #:")
        self.label.pack(pady=5)

        self.entry = tk.Entry(parent, width=40)
        self.entry.pack(pady=5)
        self.entry.bind("<Return>", self.search_images)

        # Search button
        self.search_btn = tk.Button(parent, text="Search", command=self.search_images)
        self.search_btn.pack(pady=5)

        # Scrollable canvas frame for images (fixed size 500x500)
        container = tk.Frame(parent)
        container.pack(pady=10)

        self.canvas = tk.Canvas(container, width=500, height=500, bg='white', highlightthickness=2, highlightbackground='purple', bd=1, relief='solid')
        self.canvas.grid(row=0, column=0)

        self.v_scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, command=self.canvas.yview)
        self.v_scrollbar.grid(row=0, column=1, sticky='ns')

        self.canvas.configure(yscrollcommand=self.v_scrollbar.set)

        self.results_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.results_frame, anchor='nw')

        self.results_frame.bind("<Configure>", self._on_frame_configure)

        self.save_btn = tk.Button(parent, text="Save All Images", command=self.save_all_images)
        self.save_btn.pack(pady=5)
        
        self.current_images = []

    def _on_frame_configure(self, event):
        # Update scrollregion to include whole inner frame
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def clear_results(self):
        for widget in self.results_frame.winfo_children():
            widget.destroy()

    def search_images(self, event=None):
        work_order = self.entry.get().strip()
        if not work_order:
            messagebox.showwarning("Input Needed", "Please enter a work order number.")
            return

        self.clear_results()
        records = self.db.fetch_records_by_work_order(work_order)

        if not records:
            messagebox.showinfo("No Results", f"No images found for work order: {work_order}")
            return

        for idx, (id, wo, img_blob, timestamp) in enumerate(records):
            image = Image.open(io.BytesIO(img_blob))
            self.current_images.append((image, f"{wo}_{id}.png"))
            image.thumbnail((500, 500))  # Resize images max 400x400
            photo = ImageTk.PhotoImage(image)

            lbl = tk.Label(self.results_frame, image=photo)
            lbl.image = photo  # keep a reference to prevent GC
            lbl.grid(row=idx, column=0, padx=2)

    def save_all_images(self):
        if not self.current_images:
            messagebox.showinfo("No Images", "No images to save.")
            return

        # Ask user to choose directory
        save_dir = filedialog.askdirectory(title="Select Folder to Save Images")
        if not save_dir:
            return

        for image, filename in self.current_images:
            save_path = os.path.join(save_dir, filename)
            image.save(save_path)

        messagebox.showinfo("Saved", f"Saved {len(self.current_images)} images to {save_dir}")