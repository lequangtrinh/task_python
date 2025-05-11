import tkinter as tk
from tkinter import ttk
from task_manager_ui import TaskManagerUI
from task_management_handler import TaskManager
from user_management_ui import UserManagementUI
from user_manager_handler import UserManager
class DashboardUI:
    def __init__(self, master, role, user_email):
        self.master = master
        self.master.title("Dashboard")
        self.master.state('zoomed')
        self.master.configure(bg="#f4f6f9")  # Màu nền sáng, dễ nhìn
        self.root = master
        self.role = role
        self.user_email = user_email

        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f4f6f9")
        
        # Define custom style for the Notebook tabs (default colors)
        self.style.configure("TNotebook", background="#ffffff", borderwidth=0)
        self.style.configure("TNotebook.Tab", 
                             font=("Arial", 14, "bold"), 
                             padding=[20, 10], 
                             background="#BBDEFB",  # Light blue for inactive tabs
                             foreground="black")

        # Set color for active tab and hover effect
        self.style.map("TNotebook.Tab", 
                       background=[("selected", "gray"),  # Blue when selected
                                   ("active", "gray")],  # Dark blue when active
                       foreground=[("selected", "blue"),  # White text for selected tab
                                   ("active", "blue")])  # White text for active tab

        self.frame_dashboard = tk.Frame(self.master, bg="#f4f6f9")
        self.frame_dashboard.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        self.task_manager = TaskManager(self.user_email, self.role)
        self.user_manager = UserManager(self.user_email, self.role)
        self.create_widgets()

    def create_widgets(self):
        # Title bar
        title_frame = tk.Frame(self.frame_dashboard, bg="#4CAF50", height=80)
        title_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        welcome_label = tk.Label(
            title_frame, 
            text=f"Chào mừng {self.user_email} - Vai trò: {self.role}", 
            font=("Helvetica", 16, "bold"), 
            bg="#4CAF50", 
            fg="white"
        )
        welcome_label.grid(row=0, column=0, pady=15)

        # Thêm nút Logout và Close
        logout_button = tk.Button(
            title_frame, text="Logout", command=self.logout, 
            font=("Helvetica", 12, "bold"), bg="#FF5733", fg="white", bd=0, padx=10
        )
        logout_button.grid(row=0, column=1, padx=10, pady=15)


        # Initialize TabControl widget here
        self.tab_control = ttk.Notebook(self.frame_dashboard)

        # Tab Quản lý công việc
        task_management_tab = ttk.Frame(self.tab_control, style="TFrame")  # Sử dụng style
        self.tab_control.add(task_management_tab, text=f"📝 Quản lý công việc", padding=[20, 10])
        task_management_label = tk.Label(task_management_tab, text="Quản lý công việc", font=("Arial", 14), bg="#f4f6f9")
        task_management_label.grid(row=0, column=0, pady=20)
        # Tạo TaskManagerUI trong Tab Quản lý công việc
        task_manager_ui = TaskManagerUI(task_management_tab, role=self.role, user_email=self.user_email, task_manager=self.task_manager)

        # Tab Hiển thị người dùng (Chỉ dành cho Admin và Manager)
        show_user_tab = ttk.Frame(self.tab_control, style="TFrame")  # Sử dụng style
        self.tab_control.add(show_user_tab, text=f"👤 Hiển thị người dùng", padding=[20, 10])
        
        # Label hiển thị người dùng
        show_user_label = tk.Label(show_user_tab, text="Thông tin người dùng", font=("Arial", 14), bg="#f4f6f9")
        show_user_label.grid(row=1, column=0, pady=20, padx=10)
        user_manager_ui = UserManagementUI(show_user_tab, role=self.role, user_email=self.user_email, user_manager=self.user_manager)

        # Tab Báo cáo (Có thể dành cho tất cả)
        report_tab = ttk.Frame(self.tab_control, style="TFrame")  # Sử dụng style
        self.tab_control.add(report_tab, text=f"📊 Báo cáo", padding=[20, 10])
        report_label = tk.Label(report_tab, text="Báo cáo hệ thống", font=("Arial", 14), bg="#f4f6f9")
        report_label.grid(row=0, column=0, pady=20)

        self.tab_control.grid(row=1, column=0, sticky="nsew", pady=20)

        # Chỉnh kích thước các tab cho hợp lý
        self.tab_control.tab(0, padding=[20, 10])
        self.tab_control.tab(1, padding=[20, 10])
        self.tab_control.tab(2, padding=[20, 10])

        # Thanh dưới (Footer) để thông tin thêm hoặc điều hướng khác
        footer_frame = tk.Frame(self.frame_dashboard, bg="#f4f6f9", height=40)
        footer_frame.grid(row=2, column=0, sticky="ew")
        footer_label = tk.Label(footer_frame, text="Được phát triển bởi Team X", font=("Arial", 10), bg="#f4f6f9", fg="#999999")
        footer_label.grid(row=0, column=0, pady=5)

    def logout(self):
        self.tab_control.select(0)
        for widget in self.tab_control.winfo_children():
            widget.destroy()
        self.master.withdraw()
        from application_ui import Application
        root = tk.Tk()
        app = Application(root)
        root.mainloop()



