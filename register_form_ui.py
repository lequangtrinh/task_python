import tkinter as tk
from tkinter import messagebox
from user_manager_handler import UserManager
from utils import set_background_image, create_gradient_button

class RegisterForm:
    def __init__(self, master):
        self.master = master
        self.master.title("Đăng Ký")
        self.master.geometry("400x350")
        self.user_manager = UserManager(None,None)

        self.frame = tk.Frame(self.master)
        self.frame.pack(fill="both", expand=True)
        
        # Thêm ảnh nền
        set_background_image(self.frame, "https://www.vietnamworks.com/hrinsider/wp-content/uploads/2024/01/co-4-la-1.jpeg")

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.frame, text="Tên đăng nhập:", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(pady=10)
        self.username_entry = tk.Entry(self.frame, font=("Arial", 12))
        self.username_entry.pack(pady=5)

        tk.Label(self.frame, text="Mật khẩu:", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(pady=10)
        self.password_entry = tk.Entry(self.frame, show="*", font=("Arial", 12))
        self.password_entry.pack(pady=5)

        tk.Label(self.frame, text="Email:", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(pady=10)
        self.email_entry = tk.Entry(self.frame, font=("Arial", 12))
        self.email_entry.pack(pady=5)

        create_gradient_button(self.frame, "Đăng ký", command=self.register)
        create_gradient_button(self.frame, "Quay lại", command=self.show_login_form)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        email = self.email_entry.get()

        success, message = self.user_manager.register(username, password, email)
        if success:
            messagebox.showinfo("Đăng ký thành công", message)
            self.show_login_form()  # Chuyển sang form đăng nhập
        else:
            messagebox.showerror("Lỗi đăng ký", message)

    def show_login_form(self, event=None):
        # Import LoginForm inside the method to avoid circular import
        from login_form_ui import LoginForm
        self.master.destroy()
        root = tk.Tk()
        login_form = LoginForm(root)
        root.mainloop()
