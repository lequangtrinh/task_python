import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from utils import format_date, create_form_input, on_button_hover, on_button_leave

class UserManagementUI:
    def __init__(self, parent, role, user_email, user_manager):
        self.checked_user = {}
        self.root = parent
        self.role = role
        self.user_email = user_email
        self.user_manager = user_manager
        if isinstance(self.root, tk.Tk):
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
        main_frame = tk.Frame(self.root, bg="#f7f7f7")
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.grid_columnconfigure(0, weight=1)
        return main_frame

    def create_title_label(self, parent):
        title_label = tk.Label(
            parent, text="Quản lý Người Dùng", font=("Arial", 24, "bold"), bg="#f7f7f7"
        )
        title_label.grid(row=0, column=0, pady=(0, 20), sticky="n")

    def create_controls_frame(self, parent):
        controls_frame = tk.Frame(parent, bg="#f7f7f7")
        controls_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        controls_frame.grid_columnconfigure(0, weight=1)
        controls_frame.grid_columnconfigure(1, weight=1)
        controls_frame.grid_columnconfigure(2, weight=1)
        return controls_frame

    def create_search_widgets(self, parent):
        left_frame = tk.Frame(parent, bg="#f7f7f7")
        left_frame.grid(row=0, column=0, sticky="w", padx=(0, 50))
        
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            left_frame, textvariable=self.search_var, font=("Arial", 12), width=35,
            relief="solid", bd=1
        )
        self.search_entry.grid(row=0, column=0, padx=(0, 5), pady=5)

        search_button = tk.Button(
            left_frame, text="🔍 Search", command=self.search_users,
            font=("Arial", 12, "bold"), bg="#2196F3", fg="white",
            relief="flat", cursor="hand2", padx=10, pady=5
        )
        search_button.grid(row=0, column=1, pady=5)

        self.search_entry.bind("<Return>", lambda event: self.search_users())  # Enter để tìm

    def create_create_user_button(self, parent):
        right_frame = tk.Frame(parent, bg="#f7f7f7")
        right_frame.grid(row=0, column=1, sticky="e")

        self.create_button = tk.Button(
            right_frame, text="➕ Create User", command=self.create_add_user_screen,
            font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", width=20,
            relief="flat", cursor="hand2", padx=10, pady=5
        )
        self.create_button.grid(row=0, column=0, pady=5)
        self.create_button.bind("<Enter>", on_button_hover)
        self.create_button.bind("<Leave>", on_button_leave)

    def search_users(self):
        """Tìm kiếm người dùng theo từ khóa và hiển thị kết quả"""
        keyword = self.search_var.get().lower().strip()
        filtered_users = self.user_manager.search_user(keyword)

        # Xóa các hàng cũ trong treeview
        self.clear_treeview()

        if not filtered_users:
            print("Không tìm thấy người dùng!")
            return

        # Hiển thị các người dùng tìm được trong treeview
        self.display_users_in_treeview(filtered_users)

    def clear_treeview(self):
        """Xóa tất cả các hàng trong treeview"""
        for row in self.tree.get_children():
            self.tree.delete(row)

    def display_users_in_treeview(self, filtered_users):
        """Hiển thị danh sách người dùng vào treeview"""
        for i, user in enumerate(filtered_users):
            user_email = user['email']
            user_gender = user['gender']
            user_username = user['username']
            user_role = user['role']
            user_status = "Active" if user['active'] else "Inactive"
            checkbox_symbol = "☐"
            self.checked_user[user_email] = False

            actions = "🗑️" if self.role == "admin" else "👁️"
            row_tag = "even" if i % 2 == 0 else "odd"

            self.tree.insert("", "end", values=(checkbox_symbol, user_email, user_gender, user_username, user_role, user_status, actions), tags=(row_tag,))
        self.tree.bind("<ButtonRelease-1>", self.on_tree_click)

    def create_user_management_content(self, parent):
        self.tree_frame = tk.Frame(parent, bg="#f7f7f7")
        self.tree_frame.grid(row=2, column=0, pady=20, sticky="nsew")
        self.tree = self.create_treeview(self.tree_frame)
        self.create_scrollbar(self.tree_frame)
        self.show_user()

    def create_treeview(self, parent):
        tree = ttk.Treeview(parent, columns=("Select", "Email", "Gender", "User Name", "Role", "Status", "Actions"), show="headings", height=8)
        tree.grid(row=0, column=0, pady=20, sticky="nsew")
        tree.heading("Select", text="Select")
        tree.heading("Email", text="Email")
        tree.heading("Gender", text="Gender")
        tree.heading("User Name", text="User Name")
        tree.heading("Role", text="Role")
        tree.heading("Status", text="Status")
        tree.heading("Actions", text="Actions")

        tree.column("Select", width=50, anchor="center")
        tree.column("Email", width=100, anchor="center")
        tree.column("Gender", width=50, anchor="center")
        tree.column("User Name", width=200, anchor="center")
        tree.column("Role", width=50, anchor="center")
        tree.column("Status", width=50, anchor="center")
        tree.column("Actions", width=50, anchor="center")
        return tree

    def create_scrollbar(self, parent):
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

    def show_user(self):
        users = self.user_manager.load_users()
        self.clear_treeview()

        if not users:
            print("Dữ liệu users không hợp lệ!")
            return
        if not self.user_email:
            print("Email người dùng không hợp lệ!")
            return

        filtered_users = self.filter_users_by_role(users)

        for i, (user_email, user) in enumerate(filtered_users):
            user_gender = user['gender']
            user_username = user['username']
            user_role = user['role']
            user_status = "Active" if user['active'] else "Inactive"
            checkbox_symbol = "☐"
            self.checked_user[user_email] = False
            actions = "🗑️" if self.role == "admin" else "👁️"
            row_tag = "even" if i % 2 == 0 else "odd"
            self.tree.insert("", "end", values=(checkbox_symbol, user_email, user_gender, user_username, user_role, user_status, actions), tags=(row_tag,))
        self.tree.bind("<ButtonRelease-1>", self.on_tree_click)

    def filter_users_by_role(self, users):
        """Lọc người dùng theo vai trò"""
        if self.role == "admin":
            return list(users.items())
        return [(email, user) for email, user in users.items() if user.get('email') == self.user_email]

    def on_tree_click(self, event):
        item = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)
        if not item:
            return

        values = self.tree.item(item, "values")
        email = values[1]

        if column == "#1":
            self.toggle_checkbox(email, item)
        elif column == "#6":
            self.handle_action(values, email)

    def toggle_checkbox(self, email, item):
        current_state = self.checked_user[email]
        new_state = not current_state
        self.checked_user[email] = new_state
        new_symbol = "☑" if new_state else "☐"
        new_values = list(self.tree.item(item, "values"))
        new_values[0] = new_symbol
        self.tree.item(item, values=new_values)

        if new_state:
            self.edit_task(email)

    def handle_action(self, values, email):
        actions = values[5]
        if "🗑️" in actions:
            self.delete_task(email)

    def create_add_user_screen(self):
        """Giao diện thêm người dùng"""
        self.clear_screen()
        self.add_user_frame = tk.Frame(self.root, bg="#f4f4f9")
        self.add_user_frame.pack(padx=20, pady=20)

        self.add_user_email_entry = create_form_input(self.add_user_frame, "Email:", 0)
        self.add_user_role_combobox = create_form_input(self.add_user_frame, "Vai trò:", 1, is_combobox=True, values=["user", "admin", "manage"])

        self.add_user_button = tk.Button(self.add_user_frame, text="Thêm", font=("Arial", 12), bg="#4CAF50", fg="white", command=self.add_user)
        self.add_user_button.grid(row=2, column=0, columnspan=2, pady=10)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def add_user(self):
        email = self.add_user_email_entry.get().strip()
        role = self.add_user_role_combobox.get()

        if not email or not role:
            messagebox.showerror("Error", "Vui lòng nhập đầy đủ thông tin.")
            return

        # Thêm người dùng vào cơ sở dữ liệu
        self.user_manager.add_user(email, role)
        self.show_user()
        self.clear_screen()
