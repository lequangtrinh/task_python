from PIL import Image, ImageTk
import requests
from io import BytesIO
import tkinter as tk
from datetime import datetime
from tkinter import ttk
from tkcalendar import DateEntry
def set_background_image(widget, image_url):
    try:
        response = requests.get(image_url)
        image_data = response.content
        image = Image.open(BytesIO(image_data))

        image = image.resize((widget.winfo_screenwidth(), widget.winfo_screenheight()), Image.ANTIALIAS)
        bg_image = ImageTk.PhotoImage(image)

        background_label = tk.Label(widget, image=bg_image)
        background_label.image = bg_image
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print("Lỗi khi tải ảnh nền:", e)
def create_gradient_button(master, text, width=15, height=2, command=None):
    button = tk.Button(master, text=text, width=width, height=height, command=command,
                    relief="flat", bd=0, font=("Arial", 12, "bold"),
                    fg="white", bg="#4CAF50", activebackground="#45a049", activeforeground="white")
    
    button.config(bg="#6C757D", activebackground="#343a40")
    button.pack(pady=10)
    
    return button
def format_date(date_str):
    try:
        # Nếu có cả ngày và giờ
        date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        try:
            # Nếu chỉ có ngày
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return "Invalid date format"
    
    return date_obj.strftime("%d/%m/%Y")
@staticmethod
def create_form_input(parent, label_text, row, is_combobox=False, values=None, is_date=False, is_text=False):
    label = tk.Label(parent, text=label_text, font=("Arial", 12, "bold"), bg="#f4f4f9", anchor="w")
    label.grid(row=row, column=0, sticky="w", padx=10, pady=10)

    if is_combobox:
        combobox = ttk.Combobox(parent, values=values, font=("Arial", 12), width=30)
        combobox.grid(row=row, column=1, padx=10, pady=5)
        return combobox
    elif is_date:
        date_entry = DateEntry(parent, font=("Arial", 12), width=30, date_pattern="yyyy-mm-dd", showweeknumbers=False)
        date_entry.grid(row=row, column=1, padx=10, pady=5)
        return date_entry
    elif is_text:
        text_widget = tk.Text(parent, font=("Arial", 12), width=30, height=5, wrap="word", bd=2, relief="solid")
        text_widget.grid(row=row, column=1, padx=10, pady=5)
        return text_widget
    else:
        entry = tk.Entry(parent, font=("Arial", 12), width=30)
        entry.grid(row=row, column=1, padx=10, pady=5)
        return entry
def on_button_hover(self, event):
        self.create_button.config(bg="#81C784")

def on_button_leave(self, event):
        self.create_button.config(bg="#4CAF50")