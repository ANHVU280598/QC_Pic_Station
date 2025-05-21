import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import datetime
from onvif import ONVIFCamera
from zeep.exceptions import Fault
import time
from db_handler import DBHandler
import io

class CameraApp:
    def __init__(self, root, onvif_ip, onvif_port, username, password):
        self.parent = root
        self.db = DBHandler()
        # ========== INPUT FIELD ==========
        self.input_label = tk.Label(self.parent, text="Enter Work Order #:")
        self.input_label.pack(pady=5)

        self.entry = tk.Entry(self.parent, width=60)
        self.entry.pack(pady=5)
        self.entry.focus()  # autofocus on entry

        # Bind Esc key to clear input
        self.entry.bind("<Escape>", self.clear_input)

        # Bind Enter key to take screenshot (when focused in entry)
        self.entry.bind("<Return>", self.handle_enter)

        self.entry.bind("<Key>", self.record_keypress)

        # ========== ONVIF CAMERA SETUP ==========
        self.onvif_ip = onvif_ip
        self.onvif_port = onvif_port
        self.username = username
        self.password = password

        try:
            self.cam = ONVIFCamera(self.onvif_ip, self.onvif_port, self.username, self.password)
            self.media = self.cam.create_media_service()
            self.imaging = self.cam.create_imaging_service()
            self.profile = self.media.GetProfiles()[0]
            self.token = self.profile.token
            self.video_source_token = self.media.GetVideoSources()[0].token
        except Exception as e:
            messagebox.showerror("ONVIF Error", f"Failed to connect to ONVIF camera:\n{e}")
            self.cam = None
            self.parent.destroy()
            return

        self.rtsp_url = self.get_rtsp_uri()
        if not self.rtsp_url:
            messagebox.showerror("Error", "Failed to get RTSP stream URI")
            self.parent.destroy()
            return

        self.cap = cv2.VideoCapture(self.rtsp_url, cv2.CAP_FFMPEG)

        # Video display label
        self.label = tk.Label(self.parent, bd=2, relief="solid")
        self.label.pack(pady=10)

        self.last_img_label = tk.Label(self.parent, text="Last Captured Image", bd=2, relief="groove")
        self.last_img_label.pack(pady=(5, 10))

        self.update_frame()

    def record_keypress(self, event):
        self.last_keypress_time = time.time()

    def clear_input(self, event=None):
        self.entry.delete(0, tk.END)

    def get_rtsp_uri(self):
        try:
            stream_setup = {
                'Stream': 'RTP-Unicast',
                'Transport': {'Protocol': 'RTSP'}
            }
            request = self.media.create_type('GetStreamUri')
            request.StreamSetup = stream_setup
            request.ProfileToken = self.token
            stream_uri_response = self.media.GetStreamUri(request)
            return stream_uri_response.Uri
        except Fault as fault:
            print("ONVIF Fault:", fault)
        except Exception as e:
            print("Error getting RTSP URI:", e)
        return None

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            self.current_frame = frame
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)
        self.parent.after(10, self.update_frame)

    def take_screenshot(self):
        if hasattr(self, 'current_frame'):
        # Convert frame to PNG format in memory
            success, buffer = cv2.imencode('.png', self.current_frame)
            if not success:
                messagebox.showerror("Error", "Failed to encode image")
                return

            image_bytes = buffer.tobytes()
            image = Image.open(io.BytesIO(image_bytes))

            # messagebox.showinfo("Saved", f"Screenshot saved to database")
            return image_bytes, image
        else:
            messagebox.showerror("Error", "No frame available to capture")
            return None

    def handle_enter(self, event=None):
        wo_order = self.entry.get()
        now = time.time()

        # Step 3: Take screenshot and ask for confirmation
        img, tempImg = self.take_screenshot()
        if img:
            self.awaiting_confirmation = True
            self.pending_image = img
            self.pending_work_order = wo_order
            # Display temp Img
            tempImg.thumbnail((400, 400))  # Resize for display
            photo = ImageTk.PhotoImage(tempImg)
            self.last_img_label.configure(image=photo)
            self.last_img_label.buffer = photo 

            response = messagebox.askyesno("Confirm", "Are you sure you want to save this image?\nPress Enter again to confirm, or click 'No' to cancel.")
            if not response:
                self.awaiting_confirmation = False
                self.pending_image = None
                self.pending_work_order = None
                return "break"
            else:
                # Wait for second Enter to confirm
                print("IMG")
                self.db.insert_record(self.pending_work_order, img)
                messagebox.showinfo("Saved", f"Screenshot saved for Work Order")
                self.clear_input()

                return "break"
        self.last_img_label.config(image=None)
        self.last_img_label.image = None



