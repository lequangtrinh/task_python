from datetime import datetime, timedelta
import json
import uuid
import os
class TaskManager:
    def __init__(self, user_email, role):
        self.user_email = user_email
        self.role = role  # role = 'user', 'manage', 'admin'
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        tasks_file  = os.path.join(base_dir, "data", "tasks.json")
        tasks_json = self.load_tasks_from_file(tasks_file)
        try:
            data = json.loads(tasks_json)
            self.tasks = data.get("tasks", []) 
        except json.JSONDecodeError:
            print("Lỗi khi phân tích cú pháp JSON.")
            self.tasks = []
        except KeyError:
            print('Khóa "tasks" không tồn tại trong JSON.')
            self.tasks = []      
    @staticmethod
    def load_tasks_from_file(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                tasks_json = file.read()
            return tasks_json
        except FileNotFoundError:
            print(f"Không tìm thấy tệp {file_path}.")
            return None
        except json.JSONDecodeError:
            print(f"Lỗi khi phân tích cú pháp JSON trong tệp {file_path}.")
            return None
    def save_tasks_to_file(self, file_path):
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump({"tasks": self.tasks}, file, ensure_ascii=False, indent=4)
            print(f"Tasks saved to {file_path}")
        except Exception as e:
            print(f"Error saving tasks: {e}")
    # Kiểm tra quyền người dùng khi tạo hoặc cập nhật task
    def check_role(self, assigned_to, task_id=None):
        if self.role == 'user':
            if assigned_to != self.user_email:
                return "You can only create or update tasks for yourself."
            if task_id:
                task_to_update = next((task for task in self.tasks if task["id"] == task_id), None)
                if task_to_update and task_to_update["assigned_to"] != self.user_email:
                    return "You can only update your own tasks."
        elif self.role == 'manage':
            if assigned_to == self.user_email:
                return "You cannot create tasks for yourself as a manager."
            if task_id:
                task_to_update = next((task for task in self.tasks if task["id"] == task_id), None)
                if task_to_update and task_to_update["assigned_to"] == self.user_email:
                    return "As a manager, you cannot update your own task."
        elif self.role == 'admin':
            pass
        else:
            return "Invalid role"
        return None

    # Kiểm tra thời gian bắt đầu và kết thúc có hợp lệ không
    def check_dates(self, start_date, end_date, task_id=None):
        print(end_date)
        print(start_date)
        if (end_date - start_date) < timedelta(minutes=30):
            return "End date must be at least 30 minutes after start date."
        for task in self.tasks:
            task_start_date = datetime.strptime(task["start_date"].split(" ")[0], "%Y-%m-%d")
            task_end_date = datetime.strptime(task["end_date"].split(" ")[0], "%Y-%m-%d")
            if task_id and task["id"] == task_id:
                continue
            if start_date < task_end_date.date() and end_date > task_start_date.date():
                return "There is already a task in the same time range, except for Active status tasks."
        return None
    
    # Thêm task mới
    def create_task(self, title, description, assigned_to, start_date, end_date, priority, point=0):
        role_check = self.check_role(assigned_to)
        if role_check:
            return role_check
        date_check = self.check_dates(start_date, end_date)
        if date_check:
            return date_check
        new_task = {
            "id": str(uuid.uuid4()),  # Unique ID
            "title": title,
            "description": description,
            "assigned_to": assigned_to,
            "status": "New",
            "start_date": start_date.strftime("%Y-%m-%d %H:%M:%S"),
            "end_date": end_date.strftime("%Y-%m-%d %H:%M:%S"),
            "priority": priority,
            "created_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            "is_deleted": False,
            "created_by": self.user_email,
            "updated_by": self.user_email,
            "point": point
        }
        self.tasks.append(new_task)
        self.save_tasks_to_file("tasks.json")
        return f"Task '{title}' created successfully."

    # Cập nhật task
    def update_task(self, task_id, title=None, description=None, assigned_to=None, status=None
                    , start_date=None, end_date=None, priority=None, point=None):
        role_check = self.check_role(assigned_to, task_id)
        if role_check:
            return role_check
        date_check = self.check_dates(start_date, end_date, task_id)
        if date_check:
            return date_check
        
        task_to_update = next((task for task in self.tasks if task["id"] == task_id), None)
        if not task_to_update:
            return "Task not found."

        if title:
            task_to_update["title"] = title
        if description:
            task_to_update["description"] = description
        if assigned_to:
            task_to_update["assigned_to"] = assigned_to
        if status:
            task_to_update["status"] = status
        if start_date:
            task_to_update["start_date"] = start_date.strftime("%Y-%m-%d %H:%M:%S")
        if end_date:
            task_to_update["end_date"] = end_date.strftime("%Y-%m-%d %H:%M:%S")
        if priority:
            task_to_update["priority"] = priority
        if point is not None:  # Cập nhật điểm nếu có
            task_to_update["point"] = point
        
        task_to_update["updated_at"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        task_to_update["updated_by"] = self.user_email
        self.save_tasks_to_file("tasks.json")
        return "Task updated successfully!"

    # Xóa task
    def delete_task(self, task_id):
        task_to_delete = next((task for task in self.tasks if task["id"] == task_id), None)
        if not task_to_delete:
            return "Task not found."
        role_check = self.check_role(task_to_delete["assigned_to"])
        if role_check:
            return role_check
        self.tasks = [task for task in self.tasks if task["id"] != task_id]
        self.save_tasks_to_file("tasks.json")
        return f"Task with ID {task_id} has been deleted successfully."

    # Hiển thị task dựa trên role
    def show_tasks(self):
        if self.role == 'user':
            return [task for task in self.tasks if task["assigned_to"] == self.user_email]
        elif self.role == 'manage':
            return [task for task in self.tasks if task["assigned_to"] != self.user_email]
        elif self.role == 'admin':
            return self.tasks
        return "Invalid role"
    def search_tasks_by_keyword(self, keyword):
        if not keyword:
            return []

        keyword_lower = keyword.lower()

        if self.role == 'user':
            filtered_tasks = [task for task in self.tasks if task["assigned_to"] == self.user_email]
        elif self.role == 'manage':
            filtered_tasks = [task for task in self.tasks if task["assigned_to"] != self.user_email]
        elif self.role == 'admin':
            filtered_tasks = self.tasks
        else:
            return []

        result = []
        for task in filtered_tasks:
            if (keyword_lower in task.get("title", "").lower() or
                keyword_lower in task.get("description", "").lower() or
                keyword_lower in task.get("assigned_to", "").lower() or
                keyword_lower in task.get("status", "").lower()):
                result.append(task)
        return result
