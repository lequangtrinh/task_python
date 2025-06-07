import customtkinter as ctk
from tkinter import messagebox
from tkinter.simpledialog import askstring
from handler.user_manager_handler import UserManager
from uis.register_form_ui import RegisterForm
from uis.dashboard_ui import DashboardUI

class LoginForm:
    def __init__(self, master):
        self.master = master
        self.master.title("Đăng Nhập")
        self.master.geometry("400x300")
        self.master.resizable(False, False)

        # Setup appearance
        ctk.set_appearance_mode("light")  # or "dark"
        ctk.set_default_color_theme("blue")  # or "green", "dark-blue", etc.

        self.frame = ctk.CTkFrame(self.master, corner_radius=10)
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.user_manager = UserManager(None, None)

        self.create_widgets()

    def create_widgets(self):
        self.email_entry = ctk.CTkEntry(self.frame, placeholder_text="📧 Email", width=250, height=35, corner_radius=10)
        self.email_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self.frame, placeholder_text="🔑 Mật khẩu", show="*", width=250, height=35, corner_radius=10)
        self.password_entry.pack(pady=10)

        self.show_password_var = ctk.BooleanVar()
        self.show_password_checkbox = ctk.CTkCheckBox(
            self.frame,
            text="Hiện mật khẩu",
            variable=self.show_password_var,
            command=self.toggle_password_visibility,
            width=250
        )
        self.show_password_checkbox.pack(anchor="w", padx=75, pady=(0, 10))

        forgot_label = ctk.CTkLabel(self.frame, text="Quên mật khẩu?", text_color="blue", cursor="hand2", font=("Arial", 10, "underline"))
        forgot_label.pack()
        forgot_label.bind("<Button-1>", self.forgot_password)

        self.login_button = ctk.CTkButton(
            self.frame, text="Đăng nhập", command=self.login,
            width=200, height=40, corner_radius=20,
            fg_color=("#4f93ce", "#285f8f"), text_color="white"
        )
        self.login_button.pack(pady=15)

        register_label = ctk.CTkLabel(self.frame, text="Chưa có tài khoản? Đăng ký", text_color="blue", cursor="hand2", font=("Arial", 10, "underline"))
        register_label.pack()
        register_label.bind("<Button-1>", lambda e: self.show_register_form())

    def toggle_password_visibility(self):
        if self.show_password_var.get():
            self.password_entry.configure(show="")  # Hiện mật khẩu
        else:
            self.password_entry.configure(show="*")  # Ẩn mật khẩu

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if email == "" or password == "":
            messagebox.showwarning("Lỗi", "Vui lòng nhập email và mật khẩu.")
            return
        success, result = self.user_manager.login(email, password)
        if success:
            messagebox.showinfo("Đăng nhập thành công", f"Chào mừng {result}!")
            self.master.withdraw()
            self.show_dashboard(result, email)
        else:
            messagebox.showerror("Lỗi đăng nhập", result)

    def show_register_form(self, event=None):
        self.master.withdraw()
        register_window = ctk.CTkToplevel(self.master)
        RegisterForm(register_window)
        register_window.protocol("WM_DELETE_WINDOW", self.on_register_close)

    def on_register_close(self):
        self.master.deiconify()

    def forgot_password(self, event):
        email = askstring("Quên mật khẩu", "Nhập email của bạn:")
        if email:
            success, message = self.user_manager.recover_password(email)
            messagebox.showinfo("Kết quả", message)
        else:
            messagebox.showerror("Lỗi", "Email không hợp lệ.")

    def show_dashboard(self, role, email):
        dashboard_window = ctk.CTkToplevel(self.master)
        DashboardUI(dashboard_window, role, email)
        dashboard_window.protocol("WM_DELETE_WINDOW", self.on_dashboard_close)

    def on_dashboard_close(self):
        self.master.deiconify()
