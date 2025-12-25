import cv2
import os
import sys
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD

# ---------------- CONFIG ----------------
OUTPUT_FOLDER = "output_passport"
OUTPUT_SIZE = (150, 200)  # width x height (3:4 ratio for Ghana passport)
THUMBNAIL_SIZE = (80, 80)
FACE_SCALE = 1.6  # how much extra space around face

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Correct path for PyInstaller executable
if getattr(sys, 'frozen', False):
    BASE_PATH = sys._MEIPASS
else:
    BASE_PATH = os.path.abspath(".")

CASCADE_FILE = os.path.join(BASE_PATH, "haarcascade_frontalface_default.xml")
face_cascade = cv2.CascadeClassifier(CASCADE_FILE)

# ---------------- FUNCTIONS ----------------
def process_image(image_path, bg_color=(255, 255, 255)):
    img = cv2.imread(image_path)
    if img is None:
        print(f"Skipping {image_path} (cannot read)")
        return False

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.2, minNeighbors=5, minSize=(80, 80)
    )

    if len(faces) == 0:
        print(f"No face detected: {image_path}")
        return False

    # Use largest face
    x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
    cx, cy = x + w // 2, y + h // 2
    crop_w = int(w * FACE_SCALE)
    crop_h = int(crop_w * (4 / 3))  # Passport ratio

    x1 = max(0, cx - crop_w // 2)
    y1 = max(0, cy - crop_h // 2)
    x2 = min(img.shape[1], x1 + crop_w)
    y2 = min(img.shape[0], y1 + crop_h)

    cropped = img[y1:y2, x1:x2]
    pil_img = Image.fromarray(cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB))
    pil_img = pil_img.resize(OUTPUT_SIZE, Image.LANCZOS)

    background = Image.new("RGB", OUTPUT_SIZE, bg_color)
    background.paste(pil_img)

    filename = os.path.basename(image_path)
    output_path = os.path.join(OUTPUT_FOLDER, filename)
    background.save(output_path)
    print(f"Saved: {output_path}")
    return True

# ---------------- GUI ----------------
class PassportApp:
    def __init__(self, root):
        self.root = root
        root.title("Passport Photo App")
        root.geometry("600x500")
        root.resizable(False, False)

        self.files = []
        self.thumbnails = []

        self.label = tk.Label(root, text="Drag & Drop your photos here\nor click Upload Photos",
                              width=50, height=5, bg="#f0f0f0")
        self.label.pack(pady=10)

        self.label.drop_target_register(DND_FILES)
        self.label.dnd_bind('<<Drop>>', self.drop_files)

        self.thumbnail_frame = tk.Frame(root)
        self.thumbnail_frame.pack(pady=5, fill="x")

        self.progress = ttk.Progressbar(root, orient="horizontal", length=500, mode="determinate")
        self.progress.pack(pady=10)

        self.upload_btn = tk.Button(root, text="Upload Photos", command=self.upload_files)
        self.upload_btn.pack(pady=5)

        self.start_btn = tk.Button(root, text="Start Processing", command=self.start_processing)
        self.start_btn.pack(pady=5)

    def display_thumbnails(self):
        # Clear previous thumbnails
        for widget in self.thumbnail_frame.winfo_children():
            widget.destroy()
        self.thumbnails.clear()

        for img_path in self.files:
            img = Image.open(img_path)
            img.thumbnail(THUMBNAIL_SIZE)
            tk_img = ImageTk.PhotoImage(img)
            lbl = tk.Label(self.thumbnail_frame, image=tk_img)
            lbl.image = tk_img  # keep a reference!
            lbl.pack(side="left", padx=5)
            self.thumbnails.append(tk_img)

    def upload_files(self):
        files = filedialog.askopenfilenames(title="Select Images",
                                            filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if files:
            self.files.extend(files)
            self.display_thumbnails()
            self.label.config(text=f"{len(self.files)} images ready for processing")

    def drop_files(self, event):
        files = self.root.tk.splitlist(event.data)
        self.files.extend(files)
        self.display_thumbnails()
        self.label.config(text=f"{len(self.files)} images ready for processing")

    def start_processing(self):
        if not self.files:
            messagebox.showwarning("No files", "Please upload or drag images first!")
            return

        self.progress["maximum"] = len(self.files)
        success_count = 0

        for i, file in enumerate(self.files, start=1):
            if process_image(file):
                success_count += 1
            self.progress["value"] = i
            self.root.update_idletasks()

        messagebox.showinfo("Done", f"Processed {success_count} / {len(self.files)} photos!\nCheck the '{OUTPUT_FOLDER}' folder.")
        self.progress["value"] = 0
        self.files = []
        self.display_thumbnails()
        self.label.config(text="Drag & Drop your photos here\nor click Upload Photos")

# ---------------- RUN ----------------
if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = PassportApp(root)
    root.mainloop()
