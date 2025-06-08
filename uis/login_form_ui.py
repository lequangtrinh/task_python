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
        self.master.geometry("400x350")
        self.master.resizable(False, False)
        self.dashboard_window = None
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

    def forgot_password(self, event=None):
        popup = ctk.CTkToplevel()
        popup.title("Quên mật khẩu")
        popup.geometry("350x200")
        popup.grab_set()

        label = ctk.CTkLabel(popup, text="Nhập email để khôi phục mật khẩu:")
        label.pack(pady=(20, 10))

        email_entry = ctk.CTkEntry(popup, width=250, placeholder_text="Email của bạn")
        email_entry.pack(pady=(0, 10))
        def on_close():
            popup.grab_release()
            popup.destroy()
            self.master.deiconify()
        def send_recovery():
            email = email_entry.get()
            if email:
                success, message = self.user_manager.recover_password(email)
                messagebox.showinfo("Kết quả", message)
                popup.grab_release()
                popup.destroy()
                self.master.deiconify()
            else:
                messagebox.showerror("Lỗi", "Vui lòng nhập email hợp lệ.")
        popup.protocol("WM_DELETE_WINDOW", on_close)
        submit_btn = ctk.CTkButton(popup, text="Gửi yêu cầu", command=send_recovery)
        submit_btn.pack(pady=(0, 5))

        cancel_btn = ctk.CTkButton(popup, text="Huỷ", fg_color="gray", command=popup.destroy)
        cancel_btn.pack()
    def show_dashboard(self, role, email):
        dashboard_window = ctk.CTkToplevel(self.master)
        self.dashboard_window=dashboard_window
        DashboardUI(dashboard_window, role, email)
        dashboard_window.protocol("WM_DELETE_WINDOW", self.on_dashboard_close)
    def on_dashboard_close(self):
        if messagebox.askokcancel("Thoát", "Bạn có chắc muốn đóng cửa sổ?"):
            self.dashboard_window.destroy()
            self.dashboard_window = None
        self.master.deiconify()
