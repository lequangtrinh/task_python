import customtkinter as ctk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from commons.utils import format_date, create_form_input, on_button_hover, on_button_leave

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
        self.create_widgets()

    def create_widgets(self):
        main_frame = self.create_main_frame()
        self.create_title_label(main_frame)
        controls_frame = self.create_controls_frame(main_frame)
        self.create_search_widgets(controls_frame)
        self.create_create_user_button(controls_frame)
        self.create_user_management_content(main_frame)

    def create_main_frame(self):
        main_frame = ctk.CTkFrame(self.root, fg_color="#f7f7f7")
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.grid_columnconfigure(0, weight=1)
        return main_frame

    def create_title_label(self, parent):
        title_label = ctk.CTkLabel(
            parent, text="Quản lý Người Dùng", font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, pady=(0, 20), sticky="n")

    def create_controls_frame(self, parent):
        controls_frame = ctk.CTkFrame(parent, fg_color="#f7f7f7")
        controls_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        controls_frame.grid_columnconfigure(0, weight=1)
        controls_frame.grid_columnconfigure(1, weight=1)
        return controls_frame

    def create_search_widgets(self, parent):
        left_frame = ctk.CTkFrame(parent, fg_color="#f7f7f7")
        left_frame.grid(row=0, column=0, sticky="w", padx=(0, 50))

        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(
            left_frame, textvariable=self.search_var, font=ctk.CTkFont(size=12), width=300,
            placeholder_text="Nhập từ khóa tìm kiếm"
        )
        self.search_entry.grid(row=0, column=0, padx=(0, 5), pady=5)

        search_button = ctk.CTkButton(
            left_frame, text="🔍 Search", command=self.search_users,
            font=ctk.CTkFont(size=12, weight="bold"), fg_color="#2196F3"
        )
        search_button.grid(row=0, column=1, pady=5)

        self.search_entry.bind("<Return>", lambda event: self.search_users())

    def create_create_user_button(self, parent):
        right_frame = ctk.CTkFrame(parent, fg_color="#f7f7f7")
        right_frame.grid(row=0, column=1, sticky="e")

        self.create_button = ctk.CTkButton(
            right_frame, text="➕ Create User", command=self.create_add_user_screen,
            font=ctk.CTkFont(size=12, weight="bold"), fg_color="#4CAF50", width=200
        )
        self.create_button.grid(row=0, column=0, pady=5)

    def create_user_management_content(self, parent):
        self.tree_frame = ctk.CTkFrame(parent, fg_color="#f7f7f7")
        self.tree_frame.grid(row=2, column=0, pady=20, sticky="nsew")
        self.tree = ttk.Treeview(self.tree_frame, columns=("Select", "Email", "Gender", "User Name", "Role", "Status", "Actions"), show="headings", height=8)
        self.tree.grid(row=0, column=0, sticky="nsew")

        for col in ("Select", "Email", "Gender", "User Name", "Role", "Status", "Actions"):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.show_user()

    def search_users(self):
        keyword = self.search_var.get().lower().strip()
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
        for i, (email, user) in enumerate(users.items() if isinstance(users, dict) else users):
            status = "Active" if user['active'] else "Inactive"
            checkbox = "☐"
            self.checked_user[email] = False
            action = "🗑️" if self.role == "admin" else "👁️"
            self.tree.insert("", "end", values=(checkbox, email, user['gender'], user['username'], user['role'], status, action))
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
        popup.geometry("400x350")
        popup.grab_set()  # Khóa focus popup, modal

        self.add_user_email_entry = create_form_input(popup, "Email:", 0)
        self.add_user_username_entry = create_form_input(popup, "Tên người dùng:", 1)
        self.add_user_gender_combobox = create_form_input(popup, "Giới tính:", 2, is_combobox=True, values=["Male", "Female", "Other"])
        self.add_user_role_combobox = create_form_input(popup, "Vai trò:", 3, is_combobox=True, values=["user", "admin", "manage"])

        def submit_add():
            email = self.add_user_email_entry.get().strip()
            username = self.add_user_username_entry.get().strip()
            gender = self.add_user_gender_combobox.get().strip()
            role = self.add_user_role_combobox.get().strip()

            if not email or not username or not  gender or not role:
                messagebox.showerror("Error", "Vui lòng nhập đầy đủ thông tin.")
                return
            success = self.user_manager.register(email, username, email, gender, role)
            if success:
                messagebox.showinfo("Success", "Thêm người dùng thành công.")
                popup.destroy()
                self.show_user()
            else:
                messagebox.showerror("Error", "Thêm người dùng thất bại. Email có thể đã tồn tại.")

        ctk.CTkButton(popup, text="Thêm", command=submit_add).grid(row=5, column=0, columnspan=2, pady=10)

    def edit_user(self, email):
        user = self.user_manager.get_user_by_email(email)
        if not user:
            messagebox.showerror("Error", "Không tìm thấy người dùng.")
            return

        popup = ctk.CTkToplevel(self.root)
        popup.title(f"Sửa Người Dùng: {email}")
        popup.geometry("400x300")
        popup.grab_set()  # modal

        ctk.CTkLabel(popup, text="Tên người dùng:").grid(row=0, column=0, padx=10, pady=5)
        username_entry = ctk.CTkEntry(popup)
        username_entry.grid(row=0, column=1, padx=10, pady=5)
        username_entry.insert(0, user['username'])

        ctk.CTkLabel(popup, text="Giới tính:").grid(row=1, column=0, padx=10, pady=5)
        gender_cb = ctk.CTkComboBox(popup, values=["Male", "Female", "Other"])
        gender_cb.grid(row=1, column=1, padx=10, pady=5)
        gender_cb.set(user['gender'])

        ctk.CTkLabel(popup, text="Vai trò:").grid(row=2, column=0, padx=10, pady=5)
        role_cb = ctk.CTkComboBox(popup, values=["user", "admin", "manage"])
        role_cb.grid(row=2, column=1, padx=10, pady=5)
        role_cb.set(user['role'])

        def submit_edit():
            new_username = username_entry.get().strip()
            new_gender = gender_cb.get().strip()
            new_role = role_cb.get().strip()

            if not new_username or not new_gender or not new_role:
                messagebox.showerror("Error", "Vui lòng điền đầy đủ thông tin.")
                return

            success = self.user_manager.edit_user(email, new_username, new_gender, new_role)
            if success:
                messagebox.showinfo("Success", "Cập nhật người dùng thành công.")
                popup.destroy()
                self.show_user()
            else:
                messagebox.showerror("Error", "Cập nhật người dùng thất bại.")

        ctk.CTkButton(popup, text="Cập nhật", command=submit_edit).grid(row=3, column=0, columnspan=2, pady=10)

    def delete_user(self, email):
        if messagebox.askyesno("Confirm", "Bạn có chắc chắn muốn xóa người dùng này không?"):
            success = self.user_manager.delete_user(email)
            if success:
                messagebox.showinfo("Success", "Xóa người dùng thành công.")
                self.show_user()
            else:
                messagebox.showerror("Error", "Xóa người dùng thất bại.")

