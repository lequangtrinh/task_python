import tkinter as tk
from tkinter import ttk,messagebox
from datetime import datetime
from tkcalendar import DateEntry
from handler.user_manager_handler import UserManager
import customtkinter as ctk
from commons.utils import format_date, create_form_input
class TaskManagerUI:
    def __init__(self, parent, role, user_email, task_manager):
        self.checked_tasks = {}
        self.root = parent
        self.role = role
        self.user_email = user_email
        self.task_manager = task_manager
        self.user_manager = UserManager(user_email, role)

        if isinstance(self.root, tk.Tk):
            self.root.title("Task Manager")
            self.root.state('zoomed')
            # Set default appearance mode and color theme for CustomTkinter
            ctk.set_appearance_mode("System")  # Can be "System", "Light", or "Dark"
            ctk.set_default_color_theme("blue") # Can be "blue", "green", "dark-blue"

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.create_widgets()

    def create_widgets(self):
        # Main frame using CTkFrame
        main_frame = ctk.CTkFrame(self.root, fg_color="#f7f7f7") # Use CustomTkinter frame
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.grid_columnconfigure(0, weight=1)

        # Title using CTkLabel
        ctk.CTkLabel(main_frame, text="Task Manager", font=ctk.CTkFont(family="Arial", size=28, weight="bold"),
                     text_color="#333333").grid(row=0, column=0, pady=(0, 25), sticky="n")

        # Controls Frame (search left, create right)
        controls_frame = ctk.CTkFrame(main_frame, fg_color="transparent") # Transparent frame for controls
        controls_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        controls_frame.grid_columnconfigure(0, weight=1)
        controls_frame.grid_columnconfigure(1, weight=1)

        # --- Left Side: Search Box ---
        left_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        left_frame.grid(row=0, column=0, sticky="w")

        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(
            left_frame, textvariable=self.search_var, font=ctk.CTkFont(size=14), width=350, height=35,
            placeholder_text="Tìm kiếm công việc theo từ khóa...", corner_radius=8
        )
        self.search_entry.grid(row=0, column=0, padx=(0, 10), pady=5)
        search_button = ctk.CTkButton(
            left_frame, text="🔍 Tìm kiếm", command=self.search_tasks,
            font=ctk.CTkFont(size=14, weight="bold"), fg_color="#2196F3", hover_color="#1976D2", height=35, corner_radius=8
        )
        search_button.grid(row=0, column=1, pady=5)

        self.search_entry.bind("<Return>", lambda event: self.search_tasks())

        # --- Right Side: Create Button ---
        right_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        right_frame.grid(row=0, column=1, sticky="e")

        self.create_button = ctk.CTkButton(
            right_frame, text="➕ Tạo Công Việc Mới", command=self.show_create_task_form,
            font=ctk.CTkFont(size=14, weight="bold"), fg_color="#4CAF50", hover_color="#66BB6A", width=200, height=40, corner_radius=8
        )
        self.create_button.grid(row=0, column=0)

        self.show_tasks_content(main_frame)
    def show_tasks_content(self, parent):
        tree_frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=8)
        tree_frame.grid(row=2, column=0, sticky="nsew", pady=(10, 0))
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        self.tree = ttk.Treeview(tree_frame, columns=(
            "Select","Id", "Title", "Assigned To", "Start Date", "End Date", "Point", "Priority", "Description", "Status", "Actions"),
            show="headings", height=18)
        self.tree.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        headings = {
            "Select": 50, "Id": 50, "Title": 220, "Assigned To": 150, "Start Date": 110,
            "End Date": 110, "Point": 50, "Priority": 100, "Description": 280, "Status": 100, "Actions": 50
        }
        for col, width in headings.items():
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor="center" if col in ["Select", "ID", "Point", "Actions"] else "w")

        style = ttk.Style(self.root)
        style.configure("Treeview",
                        background="white",
                        foreground="black",
                        rowheight=28,
                        fieldbackground="white",
                        font=("Segoe UI", 11))
        style.configure("Treeview.Heading",
                        font=("Segoe UI", 13, "bold"),
                        background="#4CAF50",
                        foreground="white")

        style.map('Treeview', background=[('selected', '#A5D6A7')])
        self.tree.tag_configure("completed", foreground="#155724")
        self.tree.tag_configure("in_progress", foreground="#856404")
        self.tree.tag_configure("pending", foreground="#0c5460")
        self.tree.tag_configure("done", foreground="#155724")
        self.tree.tag_configure("cancelled", foreground="#721c24")
        self.tree.tag_configure("even", background="#f9f9f9")
        self.tree.tag_configure("odd", background="white")
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"), foreground="black")
        self.show_tasks()
    def on_checkbox_click(self, task_id):
        print("edit")
    def show_create_task_form(self):
        self.task_form = tk.Toplevel(self.root)
        self.task_form.title("Tạo Công Việc Mới")
        self.task_form.geometry("750x700")
        self.task_form.config(bg="#f0f0f0")
        form_frame = ctk.CTkFrame(self.task_form, fg_color="white", corner_radius=15)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)


        user_emails = self.user_manager.get_emails_by_role()
        self.create_entries = {}
        # Danh sách trường nhập
        fields = [
            ("Tiêu Đề Công Việc:", "", False, True, None),
            ("Mô Tả Công Việc:", "", False, True, None),
            ("Ngày Bắt Đầu:", "", False, True, None),
            ("Ngày Kết Thúc:", "", False, True, None),
            ("Người Giao Công Việc (Email):", "", True, False, user_emails),
            ("Mức Độ Ưu Tiên:", "", True, False, ["Cao", "Trung Bình", "Thấp"]),
            ("Điểm Công Việc:", "", False, False, None)
        ]

        for i, field in enumerate(fields):
            label_text, value, is_combobox, is_text = field[:4]
            values = field[4] if len(field) > 4 else None
            is_date = ("Ngày Bắt Đầu" in label_text or "Ngày Kết Thúc" in label_text)

            label = ctk.CTkLabel(form_frame, text=label_text, font=("Arial", 12, "bold"), bg_color="white", anchor="w")
            label.grid(row=i, column=0, sticky="w", padx=10, pady=5)

            if label_text == "Điểm Công Việc:":
                validate_command = (self.root.register(self.validate_input), "%P")
                entry = ctk.CTkEntry(form_frame, font=("Arial", 12), width=70)
                entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            else:
                entry = create_form_input(form_frame, label_text, i,
                                        is_combobox=is_combobox, values=values,
                                        is_date=is_date, is_text=is_text)

            self.create_entries[label_text] = entry

        # Buttons
        button_frame = ctk.CTkFrame(form_frame, fg_color="white")
        button_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=30)
        save_btn = ctk.CTkButton(
            button_frame, text="💾 Lưu", font=("Arial", 12, "bold"),
            fg_color="#2196F3", hover_color="#64B5F6", width=160, height=40,
            command=lambda: self.create_task
        )
        save_btn.grid(row=0, column=0, padx=10)

        cancel_btn = ctk.CTkButton(
            button_frame, text="❌ Hủy", font=("Arial", 12, "bold"),
            fg_color="#F44336", hover_color="#EF9A9A", width=160, height=40,
            command=self.task_form.destroy
        )
        cancel_btn.grid(row=0, column=1, padx=10)
    def validate_input(self, input_value):
        if input_value == "" or input_value.isdigit():
            return True
        return False
    def on_focus_in(self, event):
        event.widget.config(bg_color="#e0f7fa")
    def on_focus_out(self, event):
        event.widget.config(bg_color="white")
    def create_task(self):
        title = self.create_entries["Tiêu Đề Công Việc:"].get()
        description = self.create_entries["Mô Tả Công Việc:"].get("1.0", "end-1c")  # Get text area content
        assigned_to = self.create_entries["Người Giao Công Việc (Email):"].get()
        start_date_str = self.create_entries["Ngày Bắt Đầu:"].get_date()  # Get the date from the calendar widget
        end_date_str = self.create_entries["Ngày Kết Thúc:"].get_date()  # Get the date from the calendar widget
        priority = self.create_entries["Mức Độ Ưu Tiên:"].get()
        point = self.create_entries["Điểm Công Việc:"].get()
        if not title or not description or not assigned_to or not start_date_str or not end_date_str or not priority or not point:
            messagebox.showerror("Missing Information", "All fields are required.")
            return
       
        result = self.task_manager.create_task(title, description, assigned_to, start_date_str, end_date_str, priority, point)
        messagebox.showinfo("Task Creation", result)
        if "successfully" in result:
            self.show_tasks()
            self.task_form.destroy()

    def clear_form(self):
        self.create_entries["Tiêu Đề Công Việc:"].delete(0, tk.END)
        self.create_entries["Mô Tả Công Việc:"].delete("1.0", "end-1c")
        self.create_entries["Người Giao Công Việc (Email):"].delete(0, tk.END)
        self.create_entries["Ngày Bắt Đầu:"].set_date('')
        self.create_entries["Ngày Kết Thúc:"].set_date('')
        self.create_entries["Mức Độ Ưu Tiên:"].delete(0, tk.END)
        self.create_entries["Điểm Công Việc:"].delete(0, tk.END)
    def show_tasks(self):
        tasks = self.task_manager.show_tasks()
        for row in self.tree.get_children():
            self.tree.delete(row)

        for i, task in enumerate(tasks):
            task_id = task['id']
            task_title = task['title']
            task_assigned_to = task['assigned_to']
            task_start_date = format_date(task['start_date'])
            task_end_date = format_date(task['end_date'])
            task_priority = task['priority']
            task_point = task['point']
            task_description = task['description']
            task_status = task['status'].lower()
            checkbox_symbol = "☐"
            self.checked_tasks[task_id] = False
            actions = ""
            if self.role == "admin":
                actions = f"🗑️"
            elif task_assigned_to == self.user_email:
                actions = "🗑️"
            status_tag_map = {
                "completed": "completed",
                "in progress": "in_progress",
                "pending": "pending",
                "done": "done",
                "cancelled": "cancelled",
                "cancelled": "cancelled"
            } 
            row_tag = "even" if i % 2 == 0 else "odd"
            status_tag = status_tag_map.get(task_status, None)
            tags = (row_tag,)
            if status_tag:
                tags = (row_tag, status_tag)
            self.tree.insert("", "end", values=(checkbox_symbol,task_id, task_title
                                                , task_assigned_to, task_start_date, task_end_date
                                                , task_point, task_priority,
                                                  task_description, task_status, actions), tags=tags)

        self.tree.bind("<ButtonRelease-1>", self.on_tree_click)

    def on_tree_click(self, event):
        item = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)
        if not item:
            return

        values = self.tree.item(item, "values")
        task_id = values[1]

        if column == "#1":
            for t_id in self.checked_tasks:
                self.checked_tasks[t_id] = False
                self.update_checkbox_display(t_id)
            current_state = self.checked_tasks[task_id]
            new_state = not current_state
            self.checked_tasks[task_id] = new_state

            new_symbol = "☑" if new_state else "☐"
            new_values = list(values)
            new_values[0] = new_symbol
            self.tree.item(item, values=new_values)

            if new_state:
                print("edit")
                self.edit_task(task_id)

        elif column == "#11":
            actions = values[10]
            if "🗑️" in actions:
                print("delete")
                self.delete_task(task_id)

    def update_checkbox_display(self, task_id):
        self.checked_tasks[task_id] = False
        for item in self.tree.get_children():
            values = self.tree.item(item, "values")
            if str(values[1]) == str(task_id):
                checkbox_display = "☑️" if self.checked_tasks.get(task_id, False) else "☐"
                new_values = list(values)
                new_values[0] = checkbox_display  
                self.tree.item(item, values=new_values)
                break
    def search_tasks(self):
        keyword = self.search_var.get().strip()
        if not keyword:
            self.show_tasks()
            return

        filtered_tasks = self.task_manager.search_tasks_by_keyword(keyword)

        for row in self.tree.get_children():
            self.tree.delete(row)

        for i, task in enumerate(filtered_tasks):
            task_id = task['id']
            task_title = task['title']
            task_assigned_to = task['assigned_to']
            task_start_date = format_date(task['start_date'])
            task_end_date = format_date(task['end_date'])
            task_priority = task['priority']
            task_point = task['point']
            task_description = task['description']
            task_status = task['status']
            checkbox_symbol = "☐"
            self.checked_tasks[task_id] = False

            actions = ""
            if self.role == "admin" or task_assigned_to == self.user_email:
                actions = "🗑️"
            status_tag_map = {
                "completed": "completed",
                "in progress": "in_progress",
                "pending": "pending",
                "done": "done",
                "cancelled": "cancelled",
                "cancelled": "cancelled"
            } 
            row_tag = "even" if i % 2 == 0 else "odd"
            status_tag = status_tag_map.get(task_status, None)
            tags = (row_tag,)
            if status_tag:
                tags = (row_tag, status_tag)
            self.tree.insert("", "end", values=(
                checkbox_symbol, task_id, task_title, task_assigned_to,
                task_start_date, task_end_date, task_point,
                task_priority, task_description, task_status, actions
            ), tags=tags)
    def edit_task(self, task_id):
        task_to_edit = next((task for task in self.task_manager.tasks if task["id"] == task_id), None)
        if not task_to_edit:
            return

        self.task_form = tk.Toplevel(self.root)
        self.task_form.title("📝 Chỉnh Sửa Công Việc")
        self.task_form.geometry("750x700")
        self.task_form.configure(bg="#f0f0f0")


        form_frame = ctk.CTkFrame(self.task_form, fg_color="white", corner_radius=15)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        user_emails = self.user_manager.get_emails_by_role()

        fields = [
            ("Tiêu Đề Công Việc:", task_to_edit["title"], False, True, None),
            ("Mô Tả Công Việc:", task_to_edit["description"], False, True, None),
            ("Ngày Bắt Đầu:", task_to_edit["start_date"], False, True, None),
            ("Ngày Kết Thúc:", task_to_edit["end_date"], False, True, None),
            ("Người Giao Công Việc (Email):", task_to_edit["assigned_to"], True, False, user_emails),
            ("Mức Độ Ưu Tiên:", task_to_edit["priority"], True, False, ["Low", "Medium", "High"]),
            ("Status:", task_to_edit["status"], True, False, ["Completed", "In Progress", "Pending", "Done", "Cancelled"]),
            ("Điểm Công Việc:", task_to_edit["point"], False, False, None)
        ]

        self.edit_entries = {}

        for i, field in enumerate(fields):
            label_text, value, is_combobox, is_text, values = field
            is_date = "Ngày Bắt Đầu" in label_text or "Ngày Kết Thúc" in label_text

            # Tạo input widget phù hợp
            if label_text == "Điểm Công Việc:":
                validate_command = (self.root.register(self.validate_input), "%P")
                entry = ctk.CTkEntry(form_frame, font=("Arial", 12), width=200, validate="key", validatecommand=validate_command)
                entry.insert(0, value)
            else:
                entry = create_form_input(form_frame, label_text, i,
                                        is_combobox=is_combobox, values=values,
                                        is_date=is_date, is_text=is_text)
                if is_date:
                    try:
                        date_obj = datetime.strptime(value.split(" ")[0], "%Y-%m-%d")
                        entry.set_date(date_obj)
                    except:
                        pass
                elif is_combobox:
                    entry.set(value)
                elif is_text:
                    entry.insert(tk.END, value)
                else:
                    entry.insert(0, value)

            self.edit_entries[label_text] = entry

        # Button Frame
        button_frame = ctk.CTkFrame(form_frame, fg_color="white")
        button_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=30)

        save_btn = ctk.CTkButton(
            button_frame, text="💾 Lưu", font=("Arial", 12, "bold"),
            fg_color="#2196F3", hover_color="#64B5F6", width=160, height=40,
            command=lambda: self.update_task(task_id)
        )
        save_btn.grid(row=0, column=0, padx=10)

        cancel_btn = ctk.CTkButton(
            button_frame, text="❌ Hủy", font=("Arial", 12, "bold"),
            fg_color="#F44336", hover_color="#EF9A9A", width=160, height=40,
            command=self.task_form.destroy
        )
        cancel_btn.grid(row=0, column=1, padx=10)
    def update_task(self, task_id):
        # Retrieving form input values
        title = self.edit_entries["Tiêu Đề Công Việc:"].get()
        description = self.edit_entries["Mô Tả Công Việc:"].get("1.0", "end-1c")  # Get text area content
        assigned_to = self.edit_entries["Người Giao Công Việc (Email):"].get()
        start_date_str = self.edit_entries["Ngày Bắt Đầu:"].get_date()  # Get the date from the calendar widget
        end_date_str = self.edit_entries["Ngày Kết Thúc:"].get_date() 
        status = self.edit_entries["Status:"].get() # Get the date from the calendar widget
        priority = self.edit_entries["Mức Độ Ưu Tiên:"].get()
        point = self.edit_entries["Điểm Công Việc:"].get()
        print(start_date_str,end_date_str)
        # Validating the input
        if not title or not description or not assigned_to or not start_date_str or not end_date_str or not priority or not point:
            messagebox.showerror("Missing Information", "All fields are required.")
            return

        # Update the task in task manager
        result=self.task_manager.update_task(task_id, title, description, assigned_to,status, start_date_str, end_date_str, priority, point)
        messagebox.showinfo("Task Update", result)
        if "successfully" in result:
            self.show_tasks()
            self.task_form.destroy()
    def delete_task(self, task_id):
        if messagebox.askyesno("Delete Task", "Are you sure you want to delete this task?"):
            self.task_manager.delete_task(task_id)
            self.show_tasks()
