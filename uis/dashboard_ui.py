import customtkinter as ctk
from tkinter import messagebox
from uis.task_manager_ui import TaskManagerUI
from handler.task_management_handler import TaskManager
from uis.user_management_ui import UserManagementUI
from handler.user_manager_handler import UserManager
from uis.report_ui import ReportUI 


class DashboardUI:
    def __init__(self, master, role, user_email):
        self.master = master
        self.master.title("Dashboard")
        self.master.state('zoomed')
        self.master.configure(bg="#f4f6f9")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.role = role
        self.user_email = user_email

        self.task_manager = TaskManager(self.user_email, self.role)
        self.user_manager = UserManager(self.user_email, self.role)

        self.frame_dashboard = ctk.CTkFrame(self.master, fg_color="#f4f6f9")
        self.frame_dashboard.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
      
        # Cấu hình grid stretch
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.frame_dashboard.grid_rowconfigure(1, weight=1)
        self.frame_dashboard.grid_columnconfigure(1, weight=1)
        
        self.create_widgets()
    def on_close(self):
        if messagebox.askokcancel("Thoát", "Bạn có chắc muốn đóng cửa sổ?"):
            self.logout
    def create_widgets(self):
        # Title bar đơn giản hóa
        title_frame = ctk.CTkFrame(self.frame_dashboard, fg_color="#4CAF50", height=60)
        title_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        title_label = ctk.CTkLabel(
            title_frame,
            text="🧩 Hệ thống quản lý công việc",
            font=ctk.CTkFont("Helvetica", 18, "bold"),
            text_color="white"
        )
        title_label.pack(pady=15, padx=20, anchor="w")

        # Sidebar menu dọc
        sidebar_frame = ctk.CTkFrame(self.frame_dashboard, width=220, fg_color="#e0e0e0")
        sidebar_frame.grid(row=1, column=0, sticky="ns", padx=10, pady=10)
        sidebar_frame.grid_propagate(False)

        # Thông tin người dùng
        user_info_frame = ctk.CTkFrame(sidebar_frame, fg_color="#ffffff", corner_radius=12)
        user_info_frame.pack(pady=(10, 20), padx=10, fill="x")
        welcome_label = ctk.CTkLabel(
                     user_info_frame,
                     text=f"{self.user_email}\nVai trò: {self.role}",
                     justify="left",
                     anchor="w",
                     font=ctk.CTkFont("Helvetica", 14, "bold"),  # Chữ đậm
                     text_color="#333333",
                     corner_radius=8,
                     padx=10,
                     pady=5
                            )                   
        welcome_label.grid(row=0, column=1, sticky="w", padx=5)

        # Các nút điều hướng
        btn_task = ctk.CTkButton(sidebar_frame, text="📝 Quản lý công việc", command=self.show_task_ui)
        btn_task.pack(fill="x", pady=5, padx=10)

        if self.role == 'admin':
            btn_user = ctk.CTkButton(sidebar_frame, text="👤 Hiển thị người dùng", command=self.show_user_ui)
            btn_user.pack(fill="x", pady=5, padx=10)

        btn_report = ctk.CTkButton(sidebar_frame, text="📊 Báo cáo", command=self.show_report_ui)
        btn_report.pack(fill="x", pady=5, padx=10)
        logout_button = ctk.CTkButton(
            sidebar_frame,
            text="👋 Đăng xuất",
            command=self.logout,
            font=ctk.CTkFont("Helvetica", 12),
            hover_color="#e74c3c",
            height=32
        )
        logout_button.pack(fill="x", pady=5, padx=10)
        # Khu vực nội dung bên phải
        self.content_frame = ctk.CTkFrame(self.frame_dashboard, fg_color="transparent")
        self.content_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        # Footer
        footer_frame = ctk.CTkFrame(self.frame_dashboard, fg_color="#f4f6f9", height=40)
        footer_frame.grid(row=2, column=0, columnspan=2, sticky="ew")
        footer_label = ctk.CTkLabel(
            footer_frame,
            text="Được phát triển bởi Team X",
            font=ctk.CTkFont(size=10),
            text_color="#999999"
        )
        footer_label.pack(pady=5)

        # Mặc định hiển thị tab Quản lý công việc
        self.show_task_ui()

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_task_ui(self):
        self.clear_content()
        TaskManagerUI(self.content_frame, role=self.role, user_email=self.user_email, task_manager=self.task_manager)

    def show_user_ui(self):
        self.clear_content()
        UserManagementUI(self.content_frame, role=self.role, user_email=self.user_email, user_manager=self.user_manager)

    def show_report_ui(self):
        self.clear_content()
        report_ui = ReportUI(
            parent=self.content_frame,
            user_handler=self.user_manager,
            task_handler=self.task_manager,
            role=self.role
        )
        report_ui.pack(fill="both", expand=True)

    def logout(self):
        self.master.destroy()
        from uis.application_ui import Application
        root = ctk.CTk()
        app = Application(root)
        root.mainloop()
