import customtkinter as ctk
from tkinter import messagebox
from user_manager_handler import UserManager

class RegisterForm:
    def __init__(self, master):
        self.master = master
        self.master.title("Đăng Ký")
        self.master.geometry("400x450")
        self.user_manager = UserManager(None, None)

        ctk.set_appearance_mode("light")  # hoặc "dark"
        ctk.set_default_color_theme("blue")

        self.frame = ctk.CTkFrame(self.master, corner_radius=10)
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.create_widgets()

    def create_widgets(self):
        # Tên đăng nhập
        username_label = ctk.CTkLabel(self.frame, text="Tên đăng nhập:")
        username_label.pack(pady=(10, 5))
        self.username_entry = ctk.CTkEntry(self.frame, width=250, height=35)
        self.username_entry.pack(pady=5)

        # Mật khẩu
        password_label = ctk.CTkLabel(self.frame, text="Mật khẩu:")
        password_label.pack(pady=(10, 5))
        self.password_entry = ctk.CTkEntry(self.frame, width=250, height=35, show="*")
        self.password_entry.pack(pady=5)

        # Email
        email_label = ctk.CTkLabel(self.frame, text="Email:")
        email_label.pack(pady=(10, 5))
        self.email_entry = ctk.CTkEntry(self.frame, width=250, height=35)
        self.email_entry.pack(pady=5)

        # Nút Đăng ký
        register_button = ctk.CTkButton(
            self.frame, text="Đăng ký", command=self.register,
            width=200, height=40, fg_color="#3b8ed0", corner_radius=20
        )
        register_button.pack(pady=(20, 10))

        # Nút Quay lại
        back_button = ctk.CTkButton(
            self.frame, text="Quay lại", command=self.show_login_form,
            width=200, height=40, fg_color="#9e9e9e", corner_radius=20
        )
        back_button.pack()

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        email = self.email_entry.get()

        success, message = self.user_manager.register(username, password, email)
        if success:
            messagebox.showinfo("Đăng ký thành công", message)
            self.show_login_form()
        else:
            messagebox.showerror("Lỗi đăng ký", message)

    def show_login_form(self, event=None):
        from login_form_ui import LoginForm
        self.master.destroy()
        root = ctk.CTk()
        LoginForm(root)
        root.mainloop()
