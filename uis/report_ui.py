# report_ui.py
import customtkinter as ctk

class ReportUI(ctk.CTkFrame):
    def __init__(self, parent, user_handler, task_handler,role, **kwargs):
        super().__init__(parent, **kwargs)
        self.user_handler = user_handler
        self.task_handler = task_handler
        self.role=role
        self.configure(fg_color="transparent")
        self.build_ui()

    def build_ui(self):
        ctk.CTkLabel(self, text="BÁO CÁO NGƯỜI DÙNG & TASK", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=15)

        role = self.role

        # USER REPORT - chỉ hiển thị nếu là admin hoặc manage
        if self.role in ["admin"]:
            user_frame = ctk.CTkFrame(self)
            user_frame.pack(pady=10, fill="x", padx=20)

            ctk.CTkLabel(user_frame, text="📊 Thống kê người dùng", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=10, pady=5)

            active, inactive = self.count_user_status()
            total_users = active + inactive
            ctk.CTkLabel(user_frame, text=f"👥 Tổng số người dùng: {total_users}", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=20, pady=(0, 5))
            ctk.CTkLabel(user_frame, text=f"🟢 Tài khoản đang hoạt động: {active}", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=20)
            ctk.CTkLabel(user_frame, text=f"🔴 Tài khoản không hoạt động: {inactive}", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=20)

        # TASK REPORT - luôn hiển thị
        task_frame = ctk.CTkFrame(self)
        task_frame.pack(pady=10, fill="x", padx=20)

        ctk.CTkLabel(task_frame, text="📌 Thống kê công việc", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=10, pady=5)

        task_stats = self.count_task_by_status()
        total_tasks = sum(task_stats.values())
        ctk.CTkLabel(task_frame, text=f"🗂️ Tổng số công việc: {total_tasks}", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=20, pady=(0, 5))

        for status, count in task_stats.items():
            ctk.CTkLabel(task_frame, text=f"• {status}: {count}", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=20)

    def count_user_status(self):
        users = self.user_handler.load_users()
        active = sum(1 for user in users.values() if user.get('active'))
        inactive = sum(1 for user in users.values() if not user.get('active'))
        return active, inactive

    def count_task_by_status(self):
        tasks = self.task_handler.show_tasks()
        status_list = ["Completed", "In Progress", "Pending", "Done", "Cancelled"]
        status_count = {status: 0 for status in status_list}

        for task in tasks:
            status = task.get("status", "Unknown")
            if status in status_count:
                status_count[status] += 1
            else:
                status_count[status] = status_count.get(status, 0) + 1
        return status_count
