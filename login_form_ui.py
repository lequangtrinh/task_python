import tkinter as tk
from tkinter import messagebox
from tkinter.simpledialog import askstring
from user_manager_handler import UserManager
from utils import create_gradient_button
from register_form_ui import RegisterForm  # Import form đăng ký
from dashboard_ui import DashboardUI  # Import DashboardUI

class LoginForm:
    def __init__(self, master):
        self.master = master
        self.master.title("Đăng Nhập")
        self.master.geometry("400x280")
        self.master.resizable(False, False)
        self.master.configure(bg="#f0f0f0")
        
        # Frame chính
        self.frame = tk.Frame(self.master, bg="#f0f0f0")
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.create_widgets()
        self.user_manager = UserManager(None,None)

    def create_widgets(self):
        # Ô nhập email
        self.email_entry = tk.Entry(self.frame, font=("Arial", 12), width=30, bd=0, highlightthickness=0)
        self.email_entry.insert(0, "📧 Email")  
        self.email_entry.bind("<FocusIn>", self.clear_email_placeholder)
        self.email_entry.bind("<FocusOut>", self.add_email_placeholder)
        self.email_entry.pack(pady=5, ipady=5)

        # Ô nhập mật khẩu
        self.password_entry = tk.Entry(self.frame, font=("Arial", 12), width=30, bd=0, highlightthickness=0, show="*")
        self.password_entry.insert(0, "🔑 Mật khẩu")  
        self.password_entry.bind("<FocusIn>", self.clear_password_placeholder)
        self.password_entry.bind("<FocusOut>", self.add_password_placeholder)
        self.password_entry.pack(pady=5, ipady=5)

        # Quên mật khẩu
        forgot_password_label = tk.Label(self.frame, text="Quên mật khẩu?", fg="blue", cursor="hand2", font=("Arial", 10, "underline"), bg="#f0f0f0")
        forgot_password_label.pack(pady=5)
        forgot_password_label.bind("<Button-1>", self.forgot_password)

        # Nút đăng nhập
        create_gradient_button(self.frame, "Đăng nhập", command=self.login)

        # Đăng ký tài khoản
        register_label = tk.Label(self.frame, text="Chưa có tài khoản? Đăng ký", fg="blue", cursor="hand2", font=("Arial", 10, "underline"), bg="#f0f0f0")
        register_label.pack(pady=5)
        register_label.bind("<Button-1>", lambda e: self.show_register_form())

    def clear_email_placeholder(self, event):
        """Xóa placeholder khi focus vào ô email"""
        if self.email_entry.get() == "📧 Email":
            self.email_entry.delete(0, "end")
            self.email_entry.config(fg="black")

    def add_email_placeholder(self, event):
        """Hiển thị placeholder nếu ô email trống khi mất focus"""
        if not self.email_entry.get():
            self.email_entry.insert(0, "📧 Email")
            self.email_entry.config(fg="gray")

    def clear_password_placeholder(self, event):
        """Xóa placeholder khi focus vào ô mật khẩu"""
        if self.password_entry.get() == "🔑 Mật khẩu":
            self.password_entry.delete(0, "end")
            self.password_entry.config(fg="black", show="*")

    def add_password_placeholder(self, event):
        """Hiển thị placeholder nếu ô mật khẩu trống khi mất focus"""
        if not self.password_entry.get():
            self.password_entry.insert(0, "🔑 Mật khẩu")
            self.password_entry.config(fg="gray", show="")

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if email == "📧 Email" or password == "🔑 Mật khẩu":
            messagebox.showwarning("Lỗi", "Vui lòng nhập email và mật khẩu.")
            return

        success, result = self.user_manager.login(email, password)
        if success:
            messagebox.showinfo("Đăng nhập thành công", f"Chào mừng {result}!")
            self.master.withdraw()  # Ẩn cửa sổ đăng nhập
            self.show_dashboard(result, email)  # Mở cửa sổ Dashboard
        else:
            messagebox.showerror("Lỗi đăng nhập", result)

    def show_register_form(self, event=None):
        """Hiển thị form đăng ký khi nhấn 'Đăng ký'"""
        self.master.withdraw()  # Ẩn cửa sổ đăng nhập
        register_window = tk.Toplevel(self.master)  # Tạo cửa sổ con mới
        register_form = RegisterForm(register_window)  # Khởi tạo form đăng ký
        register_window.protocol("WM_DELETE_WINDOW", self.on_register_close)

    def on_register_close(self):
        """Hiện lại cửa sổ đăng nhập khi đóng cửa sổ đăng ký"""
        self.master.deiconify()  # Hiện lại cửa sổ đăng nhập

    def forgot_password(self, event):
        """Quên mật khẩu - hiển thị form nhập email"""
        email = askstring("Quên mật khẩu", "Nhập email của bạn:")
        if email:
            success, message = self.user_manager.recover_password(email)
            messagebox.showinfo("Kết quả", message)
        else:
            messagebox.showerror("Lỗi", "Email không hợp lệ.")

    def show_dashboard(self, role, email):
        # Tạo cửa sổ Dashboard
        dashboard_window = tk.Toplevel(self.master)
        dashboard_ui = DashboardUI(dashboard_window, role, email)
        dashboard_window.protocol("WM_DELETE_WINDOW", self.on_dashboard_close)
    def on_dashboard_close(self):
        """Đóng cửa sổ Dashboard"""
        self.master.deiconify()  # Hiện lại cửa sổ đăng nhập

