import customtkinter as ctk
from PIL import Image, ImageTk
import requests
from io import BytesIO
from datetime import datetime
from tkcalendar import DateEntry
import tkinter as tk
def set_background_image(widget, image_url):
    try:
        response = requests.get(image_url)
        image_data = response.content
        image = Image.open(BytesIO(image_data))

        image = image.resize((widget.winfo_screenwidth(), widget.winfo_screenheight()), Image.ANTIALIAS)
        bg_image = ImageTk.PhotoImage(image)

        background_label = ctk.CTkLabel(widget, image=bg_image)
        background_label.image = bg_image
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print("Lỗi khi tải ảnh nền:", e)

def create_gradient_button(master, text, width=40, height=2, command=None):
    button = ctk.CTkButton(master, text=text, width=width, height=height, command=command,
                    font=("Arial", 12, "bold"), fg_color="#4CAF50", hover_color="#81C784",
                    active_color="#45a049", text_color="white")
    button.pack(pady=10)
    return button

def format_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return "Invalid date format"
    
    return date_obj.strftime("%d/%m/%Y")

def create_form_input(parent, label_text, row, is_combobox=False, values=None, is_date=False, is_text=False):
    label = ctk.CTkLabel(parent, text=label_text, font=("Arial", 12, "bold"), anchor="w")
    label.grid(row=row, column=0, sticky="w", padx=10, pady=10)

    if is_combobox:
        combobox = ctk.CTkComboBox(parent, values=values, font=("Arial", 12), width=200)
        combobox.grid(row=row, column=1, padx=10, pady=5)
        return combobox
    elif is_date:
        date_entry = DateEntry(parent, font=("Arial", 12), width=20, date_pattern="yyyy-mm-dd", showweeknumbers=False)
        date_entry.grid(row=row, column=1, padx=10, pady=5, sticky="w")
        return date_entry
    elif is_text:
        text_widget = ctk.CTkTextbox(parent, font=("Arial", 12), width=250, height=50, wrap="word")
        text_widget.grid(row=row, column=1, padx=10, pady=5)
        return text_widget
    else:
        entry = ctk.CTkEntry(parent, font=("Arial", 12), width=200, height=30)
        entry.grid(row=row, column=1, padx=10, pady=5)
        return entry

def on_button_hover(self, event):
    self.widget.config(fg_color="#81C784")

def on_button_leave(self, event):
    self.widget.config(fg_color="#4CAF50")
