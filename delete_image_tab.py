import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from db_handler import DBHandler
from datetime import datetime

class DeleteApp:
    def __init__(self, parent):
        self.parent = parent
        self.db = DBHandler()

        # Work Order Entry
        tk.Label(parent, text="Work Order (optional):").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.wo_entry = tk.Entry(parent, width=30)
        self.wo_entry.grid(row=0, column=1, padx=10, pady=5)

        # Date Range
        tk.Label(parent, text="Start Date:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.start_date = DateEntry(parent, width=12, background='darkblue',
                                    foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.start_date.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(parent, text="End Date:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.end_date = DateEntry(parent, width=12, background='darkblue',
                                  foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.end_date.grid(row=2, column=1, padx=10, pady=5)

        # Delete Button
        delete_btn = tk.Button(parent, text="Delete Images", command=self.delete_images)
        delete_btn.grid(row=3, column=0, columnspan=2, pady=15)

    def delete_images(self):
        wo = self.wo_entry.get().strip()
        start = self.start_date.get_date()
        end = self.end_date.get_date()

        if start > end:
            messagebox.showerror("Invalid Range", "Start date must be before end date.")
            return

        deleted = self.db.delete_records_by_criteria(wo, start, end)

        messagebox.showinfo("Done", f"Deleted {deleted} image(s).")
