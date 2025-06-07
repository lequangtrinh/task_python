import customtkinter as ctk
from tkinter import ttk, messagebox

class UserManagementUI:
    def __init__(self, parent, role, user_email, user_manager):
        self.checked_user = {}
        self.root = parent
        self.role = role
        self.user_email = user_email
        self.user_manager = user_manager
        if isinstance(self.root, ctk.CTk):
            self.root.title("Quản lý Người Dùng")
            self.root.state('zoomed')
            self.root.configure(fg_color="#e8eaf6")
        self.create_widgets()

    def create_widgets(self):
        main_frame = self.create_main_frame()
        self.create_title_label(main_frame)
        controls_frame = self.create_controls_frame(main_frame)
        self.create_search_widgets(controls_frame)
        self.create_create_user_button(controls_frame)
        self.create_user_management_content(main_frame)

    def create_main_frame(self):
        main_frame = ctk.CTkFrame(self.root, fg_color="#f5f7ff", corner_radius=12)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=30, pady=20)
        main_frame.grid_columnconfigure(0, weight=1)
        return main_frame

    def create_title_label(self, parent):
        title_label = ctk.CTkLabel(
            parent,
            text="Quản lý Người Dùng",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#344055",
            pady=15
        )
        title_label.grid(row=0, column=0, pady=(0, 25), sticky="n")

    def create_controls_frame(self, parent):
        controls_frame = ctk.CTkFrame(parent, fg_color="#f5f7ff")
        controls_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        controls_frame.grid_columnconfigure(0, weight=1)
        controls_frame.grid_columnconfigure(1, weight=0)
        return controls_frame

    def create_search_widgets(self, parent):
        left_frame = ctk.CTkFrame(parent, fg_color="#f5f7ff")
        left_frame.grid(row=0, column=0, sticky="w", padx=(0, 40))

        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(
            left_frame,
            textvariable=self.search_var,
            font=ctk.CTkFont(size=13),
            width=320,
            placeholder_text="Nhập từ khóa tìm kiếm",
            corner_radius=8,
            border_width=1,
            border_color="#b0bec5",
            fg_color="white",
            height=32
        )
        self.search_entry.grid(row=0, column=0, padx=(0, 8), pady=8)

        search_button = ctk.CTkButton(
            left_frame,
            text="🔍 Tìm kiếm",
            command=self.search_users,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#1e88e5",
            hover_color="#1565c0",
            width=110,
            height=32
        )
        search_button.grid(row=0, column=1, pady=8)

        self.search_entry.bind("<Return>", lambda event: self.search_users())

    def create_create_user_button(self, parent):
        right_frame = ctk.CTkFrame(parent, fg_color="#f5f7ff")
        right_frame.grid(row=0, column=1, sticky="e")

        self.create_button = ctk.CTkButton(
            right_frame,
            text="➕ Tạo người dùng",
            command=self.create_add_user_screen,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#43a047",
            hover_color="#2e7d32",
            width=160,
            height=32
        )
        self.create_button.grid(row=0, column=0, pady=8)

    def create_user_management_content(self, parent):
        self.tree_frame = ctk.CTkFrame(parent, fg_color="#f5f7ff", corner_radius=12)
        self.tree_frame.grid(row=2, column=0, pady=20, sticky="nsew")
        self.tree_frame.grid_rowconfigure(0, weight=1)
        self.tree_frame.grid_columnconfigure(0, weight=1)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview",
                        background="#ffffff",
                        foreground="#344055",
                        rowheight=30,
                        fieldbackground="#f5f7ff",
                        font=('Segoe UI', 11))
        style.map('Treeview', background=[('selected', '#90caf9')])

        self.tree = ttk.Treeview(
            self.tree_frame,
            columns=("Select", "Email", "Gender", "User Name", "Role", "Status", "Actions"),
            show="headings",
            height=9
        )
        self.tree.grid(row=0, column=0, sticky="nsew")

        headings = {
            "Select": 50,
            "Email": 220,
            "Gender": 120,
            "User Name": 180,
            "Role": 90,
            "Status": 90,
            "Actions": 80
        }
        for col, width in headings.items():
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor="center" if col in ["Select", "Actions"] else "w")

        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.show_user()

    def search_users(self):
        keyword = self.search_var.get().lower().strip()
        if not keyword:
            self.show_user()
            return
        filtered_users = self.user_manager.search_user(keyword)
        self.clear_treeview()
        if filtered_users:
            self.display_users_in_treeview(filtered_users)

    def show_user(self):
        users = self.user_manager.load_users()
        self.clear_treeview()
        if users and self.user_email:
            filtered = self.filter_users_by_role(users)
            self.display_users_in_treeview(filtered)

    def display_users_in_treeview(self, users):
        self.checked_user = {}

        if isinstance(users, dict):
            users = list(users.values())

        for i, user in enumerate(users):
            email = user.get("email", f"unknown_{i}")
            status = "Active" if user.get("active") else "Inactive"
            checkbox = "☐"
            self.checked_user[email] = False
            action = "🗑️" if self.role == "admin" else "👁️"
            self.tree.insert("", "end", values=(
                checkbox, email, user.get('gender', ''), user.get('username', ''), user.get('role', ''), status, action
            ))

        self.tree.bind("<ButtonRelease-1>", self.on_tree_click)

    def clear_treeview(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

    def filter_users_by_role(self, users):
        if self.role == "admin":
            return users
        return {email: user for email, user in users.items() if email == self.user_email}

    def on_tree_click(self, event):
        item = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)
        if not item:
            return
        values = self.tree.item(item, "values")
        email = values[1]
        if column == "#1":
            self.toggle_checkbox(email, item)
        elif column == "#7":
            self.handle_action(values, email)

    def toggle_checkbox(self, email, item):
        for e in self.checked_user:
            self.checked_user[e] = False
            self.update_checkbox_display(e)
        self.checked_user[email] = not self.checked_user[email]
        symbol = "☑" if self.checked_user[email] else "☐"
        values = list(self.tree.item(item, "values"))
        values[0] = symbol
        self.tree.item(item, values=values)
        if self.checked_user[email]:
            self.edit_user(email)

    def update_checkbox_display(self, email):
        for item in self.tree.get_children():
            values = self.tree.item(item, "values")
            if values[1] == email:
                values = list(values)
                values[0] = "☑" if self.checked_user[email] else "☐"
                self.tree.item(item, values=values)

    def handle_action(self, values, email):
        if "🗑️" in values[6]:
            self.delete_user(email)

    def create_add_user_screen(self):
        popup = ctk.CTkToplevel(self.root)
        popup.title("Thêm Người Dùng")
        popup.geometry("500x350")
        popup.grab_set()
        popup.configure(fg_color="#f5f7ff")

        # Các label + input
        ctk.CTkLabel(popup, text="Email:", font=ctk.CTkFont(size=13)).grid(row=0, column=0, padx=15, pady=12, sticky="w")
        self.add_user_email_entry = ctk.CTkEntry(popup, width=280, font=ctk.CTkFont(size=12))
        self.add_user_email_entry.grid(row=0, column=1, pady=12, sticky="ew")

        ctk.CTkLabel(popup, text="Tên người dùng:", font=ctk.CTkFont(size=13)).grid(row=1, column=0, padx=15, pady=12, sticky="w")
        self.add_user_username_entry = ctk.CTkEntry(popup, width=280, font=ctk.CTkFont(size=12))
        self.add_user_username_entry.grid(row=1, column=1, pady=12, sticky="ew")

        ctk.CTkLabel(popup, text="Giới tính:", font=ctk.CTkFont(size=13)).grid(row=2, column=0, padx=15, pady=12, sticky="w")
        self.add_user_gender_var = ctk.StringVar(value="Nam")
        gender_option = ctk.CTkOptionMenu(popup, values=["Nam", "Nữ", "Khác"], variable=self.add_user_gender_var, width=150)
        gender_option.grid(row=2, column=1, pady=12, sticky="ew")

        ctk.CTkLabel(popup, text="Quyền:", font=ctk.CTkFont(size=13)).grid(row=3, column=0, padx=15, pady=12, sticky="w")
        self.add_user_role_var = ctk.StringVar(value="user")
        role_option = ctk.CTkOptionMenu(popup, values=["admin", "user"], variable=self.add_user_role_var, width=150)
        role_option.grid(row=3, column=1, pady=12, sticky="ew")

        active_var = ctk.BooleanVar(value=True)
        self.add_user_active_check = ctk.CTkCheckBox(popup, text="Kích hoạt", variable=active_var)
        self.add_user_active_check.grid(row=4, column=1, sticky="w", padx=15, pady=10)

        btn_frame = ctk.CTkFrame(popup, fg_color="#f5f7ff")
        btn_frame.grid(row=5, column=0, columnspan=2, pady=20)

        submit_btn = ctk.CTkButton(btn_frame, text="Thêm", width=120, command=lambda: self.add_user(popup))
        submit_btn.grid(row=0, column=0, padx=15)

        cancel_btn = ctk.CTkButton(btn_frame, text="Hủy", width=120, fg_color="#e53935", hover_color="#b71c1c", command=popup.destroy)
        cancel_btn.grid(row=0, column=1, padx=15)

    def add_user(self, popup):
        email = self.add_user_email_entry.get().strip()
        username = self.add_user_username_entry.get().strip()
        gender = self.add_user_gender_var.get()
        role = self.add_user_role_var.get()
        active = self.add_user_active_check.get()

        if not email or not username:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ Email và Tên người dùng.")
            return

        success = self.user_manager.add_user(email, {
            "email": email,
            "username": username,
            "gender": gender,
            "role": role,
            "active": active
        })
        if success:
            messagebox.showinfo("Thành công", "Thêm người dùng thành công.")
            popup.destroy()
            self.show_user()
        else:
            messagebox.showerror("Lỗi", "Email đã tồn tại hoặc không thể thêm người dùng.")

    def edit_user(self, email):
        user = self.user_manager.get_user_by_email(email)
        if not user:
            messagebox.showerror("Lỗi", "Người dùng không tồn tại.")
            return

        popup = ctk.CTkToplevel(self.root)
        popup.title(f"Sửa Người Dùng - {email}")
        popup.geometry("500x350")
        popup.grab_set()
        popup.configure(fg_color="#f5f7ff")

        ctk.CTkLabel(popup, text="Tên người dùng:", font=ctk.CTkFont(size=13)).grid(row=1, column=0, padx=15, pady=12, sticky="w")
        self.edit_user_username_entry = ctk.CTkEntry(popup, width=280, font=ctk.CTkFont(size=12))
        self.edit_user_username_entry.insert(0, user.get("username", ""))
        self.edit_user_username_entry.grid(row=1, column=1, pady=12, sticky="ew")

        ctk.CTkLabel(popup, text="Giới tính:", font=ctk.CTkFont(size=13)).grid(row=2, column=0, padx=15, pady=12, sticky="w")
        self.edit_user_gender_var = ctk.StringVar(value=user.get("gender", "Nam"))
        gender_option = ctk.CTkOptionMenu(popup, values=["Nam", "Nữ", "Khác"], variable=self.edit_user_gender_var, width=150)
        gender_option.grid(row=2, column=1, pady=12, sticky="ew")

        ctk.CTkLabel(popup, text="Quyền:", font=ctk.CTkFont(size=13)).grid(row=3, column=0, padx=15, pady=12, sticky="w")
        self.edit_user_role_var = ctk.StringVar(value=user.get("role", "user"))
        role_option = ctk.CTkOptionMenu(popup, values=["admin", "user"], variable=self.edit_user_role_var, width=150)
        role_option.grid(row=3, column=1, pady=12, sticky="ew")

        active_var = ctk.BooleanVar(value=user.get("active", True))
        self.edit_user_active_check = ctk.CTkCheckBox(popup, text="Kích hoạt", variable=active_var)
        self.edit_user_active_check.grid(row=4, column=1, sticky="w", padx=15, pady=10)

        btn_frame = ctk.CTkFrame(popup, fg_color="#f5f7ff")
        btn_frame.grid(row=5, column=0, columnspan=2, pady=20)

        submit_btn = ctk.CTkButton(btn_frame, text="Lưu", width=120, command=lambda: self.save_user_edit(popup, email))
        submit_btn.grid(row=0, column=0, padx=15)

        cancel_btn = ctk.CTkButton(btn_frame, text="Hủy", width=120, fg_color="#e53935", hover_color="#b71c1c", command=popup.destroy)
        cancel_btn.grid(row=0, column=1, padx=15)

    def save_user_edit(self, popup, email):
        username = self.edit_user_username_entry.get().strip()
        gender = self.edit_user_gender_var.get()
        role = self.edit_user_role_var.get()
        active = self.edit_user_active_check.get()

        if not username:
            messagebox.showwarning("Thiếu thông tin", "Tên người dùng không được để trống.")
            return

        success = self.user_manager.update_user(email, {
            "username": username,
            "gender": gender,
            "role": role,
            "active": active
        })
        if success:
            messagebox.showinfo("Thành công", "Cập nhật người dùng thành công.")
            popup.destroy()
            self.show_user()
        else:
            messagebox.showerror("Lỗi", "Không thể cập nhật người dùng.")

    def delete_user(self, email):
        confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa người dùng {email}?")
        if confirm:
            success = self.user_manager.delete_user(email)
            if success:
                messagebox.showinfo("Thành công", "Xóa người dùng thành công.")
                self.show_user()
            else:
                messagebox.showerror("Lỗi", "Không thể xóa người dùng.")