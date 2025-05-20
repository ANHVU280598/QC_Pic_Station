import tkinter as tk
from tkinter import ttk
from cam_app import CameraApp  # <-- your class above saved in camera_app.py
from search_app import SearchApp

def main():
    root = tk.Tk()
    root.title("QC Pic Station Tabs")
    root.geometry("900x900")

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    tab1 = ttk.Frame(notebook)
    tab2 = ttk.Frame(notebook)
    tab3 = ttk.Frame(notebook)

    notebook.add(tab1, text="Capture")
    notebook.add(tab2, text="Search")
    notebook.add(tab3, text="Delete Image")

    # 🎯 Pass tab1 as the parent to CameraApp
    onvif_ip = "192.168.100.112"
    onvif_port = 80
    username = "admin"
    password = "Password1"
    cam_app = CameraApp(tab1, onvif_ip, onvif_port, username, password)
    
    search_app = SearchApp(tab2)

    # Placeholder in tab2
    # ttk.Label(tab2, text="Search Images by Work Order").pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
