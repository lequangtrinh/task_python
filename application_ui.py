import tkinter as tk
from login_form_ui import LoginForm
from register_form_ui import RegisterForm

class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng Dụng Quản Lý Tài Khoản")
        self.root.geometry("800x500")
        self.show_login_form()

    def show_login_form(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        LoginForm(self.root)

    def show_register_form(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        RegisterForm(self.root)
