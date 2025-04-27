import tkinter as tk
from tkinter import ttk,messagebox
from datetime import datetime
from tkcalendar import DateEntry
from user_manager_handler import UserManager
from utils import format_date, create_form_input,on_button_hover,on_button_leave
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

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.create_widgets()
    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg="#f7f7f7")
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.grid_columnconfigure(0, weight=1)

        # Title
        tk.Label(main_frame, text="Task Manager", font=("Arial", 24, "bold"), bg="#f7f7f7")\
            .grid(row=0, column=0, pady=(0, 20), sticky="n")

        # Controls Frame (search left, create right)
        controls_frame = tk.Frame(main_frame, bg="#f7f7f7")
        controls_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        controls_frame.grid_columnconfigure(0, weight=1)
        controls_frame.grid_columnconfigure(1, weight=1)

        # --- Left Side: Search Box ---
        left_frame = tk.Frame(controls_frame, bg="#f7f7f7")
        left_frame.grid(row=0, column=0, sticky="w")

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(left_frame, textvariable=self.search_var, font=("Arial", 12), width=30)
        self.search_entry.grid(row=0, column=0, padx=(0, 5))

        search_button = tk.Button(
            left_frame, text="Search", command=self.search_tasks,
            font=("Arial", 12), bg="#2196F3", fg="white", relief="flat", cursor="hand2"
        )
        search_button.grid(row=0, column=1)

        self.search_entry.bind("<Return>", lambda event: self.search_tasks())  # Optional: Enter to search

        # --- Right Side: Create Button ---
        right_frame = tk.Frame(controls_frame, bg="#f7f7f7")
        right_frame.grid(row=0, column=1, sticky="e")

        self.create_button = tk.Button(
            right_frame, text="Create Task", command=self.show_create_task_form,
            font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", width=20,
            relief="flat", cursor="hand2"
        )
        self.create_button.grid(row=0, column=0)

        self.create_button.bind("<Enter>", on_button_hover)
        self.create_button.bind("<Leave>", on_button_leave)

        # Show task list
        self.show_tasks_content(main_frame)

    def show_tasks_content(self, parent):
        self.tree_frame = tk.Frame(parent, bg="#f7f7f7")
        self.tree_frame.grid(row=2, column=0, pady=20, sticky="nsew")

        self.tree = ttk.Treeview(self.tree_frame, columns=("Select", "ID", "Title", "Assigned To"
                                                           , "Start Date", "End Date","Point"
                                                           , "Priority", "Description", "Status", "Actions"), show="headings", height=16)
        self.tree.grid(row=0, column=0, pady=20, sticky="nsew")

        self.scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.tree.heading("Select", text="Select")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Assigned To", text="Assigned To")
        self.tree.heading("Start Date", text="Start Date")
        self.tree.heading("End Date", text="End Date")
        self.tree.heading("Point", text="Point")
        self.tree.heading("Priority", text="Priority")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Actions", text="Actions")

        self.tree.column("Select", width=50, anchor="center")
        self.tree.column("ID", width=80, anchor="center")
        self.tree.column("Title", width=200)
        self.tree.column("Assigned To", width=150)
        self.tree.column("Start Date", width=120)
        self.tree.column("End Date", width=120)
        self.tree.column("Point", width=50, anchor="center")
        self.tree.column("Priority", width=100)
        self.tree.column("Description", width=250)
        self.tree.column("Status", width=100)
        self.tree.column("Actions", width=50, anchor="center")

        self.style = ttk.Style()
        self.style.configure("Treeview",
                            background="#f7f7f7",
                            foreground="black",
                            font=("Arial", 12),
                            rowheight=25)
        self.style.configure("Treeview.Heading",
                            font=("Arial", 13, "bold"),
                            background="#4CAF50",
                            foreground="black")

        self.tree.tag_configure("even", background="#f2f2f2")
        self.tree.tag_configure("odd", background="#ffffff")

        self.show_tasks()
    def on_checkbox_click(self, task_id):
        print("edit")
    def show_create_task_form(self):
        self.task_form = tk.Toplevel(self.root)
        self.task_form.title("Tạo Công Việc Mới")
        self.task_form.geometry("700x500")
        self.task_form.config(bg="#ffffff")

        form_frame = tk.Frame(self.task_form, bg="white")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        user_emails = self.user_manager.get_emails_by_role()
        # Danh sách trường nhập
        fields = [
            ("Tiêu Đề Công Việc:", "", False, False, None),
            ("Mô Tả Công Việc:", "", False, True, None),
            ("Ngày Bắt Đầu:", "", False, True, None),
            ("Ngày Kết Thúc:", "", False, True, None),
            ("Người Giao Công Việc (Email):", "", True, False,  user_emails),
            ("Mức Độ Ưu Tiên:", "", True, False, ["Cao", "Trung Bình", "Thấp"]),
            ("Điểm Công Việc:", "", False, False, None)
        ]

        self.create_entries = {}

        for i, field in enumerate(fields):
            label_text, value, is_combobox, is_text = field[:4]
            values = field[4] if len(field) > 4 else None 
            is_date = ("Ngày Bắt Đầu" in label_text or "Ngày Kết Thúc" in label_text)

            label = tk.Label(form_frame, text=label_text, font=("Arial", 12, "bold"), bg="white", anchor="w")
            label.grid(row=i, column=0, sticky="w", padx=10, pady=5)

            if label_text == "Điểm Công Việc:":
                entry = tk.Spinbox(form_frame, from_=0, to=10, increment=0.5,width=15) 
                entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            else:
                entry = create_form_input(form_frame, label_text, i,
                                    is_combobox=is_combobox, values=values,
                                    is_date=is_date, is_text=is_text)

            self.create_entries[label_text] = entry

        # Buttons
        button_frame = tk.Frame(form_frame, bg="white")
        button_frame.grid(row=len(fields) + 1, column=0, columnspan=2, pady=20)

        save_btn = tk.Button(button_frame, text="💾 Lưu", font=("Arial", 12, "bold"),
                            bg="#4CAF50", fg="white", padx=20, command=self.create_task)
        save_btn.pack(side="left", padx=10)

        cancel_btn = tk.Button(button_frame, text="❌ Hủy", font=("Arial", 12, "bold"),
                            bg="#F44336", fg="white", padx=20, command=self.task_form.destroy)
        cancel_btn.pack(side="left", padx=10)
  
    def on_focus_in(self, event):
        event.widget.config(bg="#e0f7fa")

    def on_focus_out(self, event):
        event.widget.config(bg="white")

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
            task_status = task['status']
            checkbox_symbol = "☐"
            self.checked_tasks[task_id] = False
            actions = ""
            if self.role == "admin":
                actions = f"🗑️"
            elif task_assigned_to == self.user_email:
                actions = "🗑️"
            
            row_tag = "even" if i % 2 == 0 else "odd"
            self.tree.insert("", "end", values=(checkbox_symbol,task_id, task_title, task_assigned_to, task_start_date, task_end_date, task_point, task_priority, task_description, task_status, actions), tags=(row_tag,))

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

        # Xóa dữ liệu cũ trên Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Hiển thị lại dữ liệu đã lọc
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

            row_tag = "even" if i % 2 == 0 else "odd"
            self.tree.insert("", "end", values=(
                checkbox_symbol, task_id, task_title, task_assigned_to,
                task_start_date, task_end_date, task_point,
                task_priority, task_description, task_status, actions
            ), tags=(row_tag,))
    def edit_task(self, task_id):
        task_to_edit = next((task for task in self.task_manager.tasks if task["id"] == task_id), None)
        if task_to_edit:
            # Create top-level window for editing task
            self.task_form = tk.Toplevel(self.root)
            self.task_form.title("Chỉnh Sửa Công Việc")
            self.task_form.geometry("700x500")
            self.task_form.config(bg="#ffffff")

            # Form layout
            form_frame = tk.Frame(self.task_form, bg="white")
            form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            user_emails = self.user_manager.get_emails_by_role()
            # Fields definition with the data from the task to edit
            fields = [
                    ("Tiêu Đề Công Việc:", task_to_edit["title"], False, False, None),
                    ("Mô Tả Công Việc:", task_to_edit["description"], False, True, None),
                    ("Ngày Bắt Đầu:", task_to_edit["start_date"], False, True, None),
                    ("Ngày Kết Thúc:", task_to_edit["end_date"], False, True, None),
                    ("Người Giao Công Việc (Email):", task_to_edit["assigned_to"], True, False, user_emails),
                    ("Mức Độ Ưu Tiên:", task_to_edit["priority"], True, False, ["Low", "Medium", "High"]),
                    ("Status:", task_to_edit["status"], True, False, ["Completed", "In Progress", "Pending","Done"]),
                    ("Điểm Công Việc:", task_to_edit["point"], False, False, None)
                   ]
            self.edit_entries = {}
            for i, field in enumerate(fields):
                label_text, value, is_combobox, is_text = field[:4]
                values = field[4] if len(field) > 4 else None 
                is_date = ("Ngày Bắt Đầu" in label_text or "Ngày Kết Thúc" in label_text)
                label = tk.Label(form_frame, text=label_text, font=("Arial", 12, "bold"), bg="white", anchor="w")
                label.grid(row=i, column=0, sticky="w", padx=5, pady=5)
                row = i
                if label_text == "Điểm Công Việc:":
                    entry = tk.Spinbox(form_frame, from_=0, to=10, increment=0.5, width=15)
                    entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
                    entry.delete(0, tk.END)
                else:
                    entry = create_form_input(form_frame, label_text, i,
                                        is_combobox=is_combobox, values=values,
                                        is_date=is_date, is_text=is_text)
                if is_date:
                    if isinstance(value, str):
                        value = value.split(" ")[0] 
                    try:
                        date_obj = datetime.strptime(value, "%Y-%m-%d")
                        formatted_date = date_obj.strftime("%m/%d/%Y")  # Format to MM/DD/YYYY
                    except ValueError:
                        formatted_date = value  # If it doesn't parse correctly, use the original value

                    
                    entry.set_date(date_obj)  # Set the date value using set_date()
                elif is_combobox and values:
                    print("combobox",value)
                    entry.set(value)
                elif is_text:
                    print("is_text",value)
                    entry.insert(tk.END, value)
                if not is_combobox and not is_date and not is_text:
                    print("end",value)
                    entry.delete(0, tk.END)
                    entry.insert(0, value)  # Set the value for entry widgets

                self.edit_entries[label_text] = entry

            # Buttons (Lưu, Hủy)
            button_frame = tk.Frame(form_frame, bg="white")
            button_frame.grid(row=len(fields) + 1, column=0, columnspan=2, pady=20)

            save_btn = tk.Button(button_frame, text="💾 Lưu", font=("Arial", 12, "bold"),
                                bg="#4CAF50", fg="white", padx=20, command=lambda: self.update_task(task_id))
            save_btn.pack(side="left", padx=10)

            cancel_btn = tk.Button(button_frame, text="❌ Hủy", font=("Arial", 12, "bold"),
                                bg="#F44336", fg="white", padx=20, command=self.task_form.destroy)
            cancel_btn.pack(side="left", padx=10)

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
