import hashlib
import json
import os
from datetime import datetime
from email.message import EmailMessage
import smtplib
import sys
def hash_md5(password):
    return hashlib.md5(password.encode()).hexdigest()

class UserManager:
    def __init__(self, user_email,role):
        self.user_email = user_email
        self.role = role
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.user_file = self.resource_path(os.path.join("data", "users.json"))
        print(self.user_file)
        self.users = self.load_users()
    def resource_path(self,relative_path):
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path) 
    def load_users(self):
        if not os.path.exists(self.user_file):
            return {}
        with open(self.user_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            users = {}
            for user_info in data["data"]:
                if not user_info['is_delete']:  # Chỉ thêm người dùng không bị xóa
                    users[user_info['email']] = {
                        'password': user_info['password'],
                        'email': user_info['email'],
                        'role': user_info['role'],
                        'username': user_info['username'],
                        'gender': user_info['gender'],
                        'create_at': user_info['create_at'],
                        'update_at': user_info['update_at'],
                        'is_delete': user_info['is_delete'],
                        'active': user_info['active']
                    }

        return users
    
    def save_users(self):
        """Lưu danh sách người dùng vào file"""
        with open(self.user_file, 'w', encoding='utf-8') as f:
            json.dump({"data": list(self.users.values())}, f, indent=4)

    def check_email_exists(self, email):
        return email in self.users

    def register(self, username, password, email, role='user', gender='Male'):
        """Đăng ký tài khoản mới"""
        if self.check_email_exists(email):
            return False, "Email đã tồn tại."
        
        self.users[email] = {
            'password': hash_md5(password),
            'email': email,
            'role': role,
            'username': username,
            'gender': gender,
            'create_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'update_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'is_delete': False,
            'active': True
        }
        self.save_users()
        return True, "Đăng ký thành công."

    def login(self, email, password):
        """Đăng nhập"""
        if self.check_email_exists(email):
            user_info = self.users[email]
            if user_info['is_delete']:
                return False, "Tài khoản đã bị xóa."
            if not user_info['active']:
                return False, "Tài khoản chưa được kích hoạt."
            
            if user_info['password'] == hash_md5(password):
                return True, user_info['role']
            else:
                return False, "Mật khẩu sai."
        return False, "Email không tồn tại."

    def recover_password(self, email):
        """Khôi phục mật khẩu và gửi email với mật khẩu mặc định"""
        if not self.check_email_exists(email):
            return False, "Email không tồn tại."

        user_info = self.users[email]
        default_password = "11111"
        self.users[email]['password'] = hash_md5(default_password)
        self.save_users()

        subject = "Khôi phục mật khẩu"
        body = f"Chào {user_info['email']},\n\nMật khẩu mới của bạn là: {default_password}\nVui lòng thay đổi mật khẩu sau khi đăng nhập."
        return True, f"Mật khẩu mới đã được gửi đến email {email}."
        # if self.send_email(user_info['email'], subject, body):
        #     return True, f"Mật khẩu mới đã được gửi đến email {email}."
        # else:
        #     return False, "Gửi email không thành công."

    def send_email(self, to_email, subject, body):
        from_email = "lequangtrinh0811@gmail.com"
        from_password = "$Trinh123"
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(from_email, from_password)
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False

    # Sửa thông tin người dùng
    def edit_user(self, old_email, new_email=None, new_role=None, new_username=None, new_gender=None, new_active=None):
        if old_email in self.users:
            if new_email and new_email != old_email:
                if self.check_email_exists(new_email):
                    return False, "Email mới đã tồn tại trong hệ thống."
                self.users[old_email]['email'] = new_email
            
            if new_username:
                self.users[old_email]['username'] = new_username
            if new_gender:
                self.users[old_email]['gender'] = new_gender
            if new_role:
                self.users[old_email]['role'] = new_role
            if new_active is not None:
                self.users[old_email]['active'] = new_active  # Chỉnh sửa trạng thái active
            self.users[old_email]['update_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            self.save_users()
            return True, "Người dùng đã được cập nhật."
        
        return False, "Người dùng không tồn tại."
    def get_user_by_email(self, email):
        return self.users.get(email)
    def delete_user(self, email):
        """Xóa người dùng khỏi hệ thống"""
        if email in self.users:
            self.users[email]['is_delete'] = True
            self.save_users()
            return True, f"Người dùng {email} đã được xóa."
        return False, "Người dùng không tồn tại."
    def search_user(self, keyword):
        keyword = keyword.lower().strip()
        results = []

        # Nếu là user hoặc manage, chỉ tìm kiếm chính mình hoặc người khác
        if self.role in ['user', 'manage']:
            for user in self.users.values():
                if (
                    keyword in user['email'].lower() or 
                    keyword in user['username'].lower() or
                    keyword in user['role'].lower()
                ):
                    # Nếu là user, chỉ tìm kiếm người dùng hiện tại
                    if self.role == 'user' and user['email'] == self.user_email:
                        results.append(user)
                    # Nếu là manage, chỉ tìm kiếm người dùng khác
                    elif self.role == 'manage' and user['email'] != self.user_email:
                        results.append(user)
        elif self.role == 'admin':
            for user in self.users.values():
                if (
                    keyword in user['email'].lower() or 
                    keyword in user['username'].lower() or
                    keyword in user['role'].lower()
                ):
                    results.append(user)

        return results
    def get_emails_by_role(self):
        emails = []
        if self.role == 'admin':
            emails = [user['email'] for user in self.users.values()]
        
        # If the role is user, only load the email of the current user
        elif self.role == 'user':
            if self.user_email in self.users:
                emails.append(self.user_email)
        elif self.role == 'manage':
            emails.append(self.user_email)

            for email, user in self.users.items():
                if user['role'] == 'user' and user['email'] != self.user_email:
                    emails.append(email)
        return emails