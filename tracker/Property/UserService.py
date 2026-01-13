
# ===== app.py (Main Flask Application) =====
"""
Expense Tracker - Complete Flask App with Microservices
For PythonAnywhere deployment
"""
from datetime import datetime
from util import load_json, save_json, DATA_DIR, USERS_FILE, EXPENSES_FILE

# ===== MICROSERVICE: USER SERVICE =====
class UserService:
    @staticmethod
    def get_all_users():
        return load_json(USERS_FILE)
    
    @staticmethod
    def get_user(username):
        users = load_json(USERS_FILE)
        return next((u for u in users if u['username'] == username), None)
    
    @staticmethod
    def create_user(username, password):
        users = load_json(USERS_FILE)
        
        if any(u['username'] == username for u in users):
            return {'success': False, 'message': 'Username already exists'}
        
        user = {
            'id': len(users) + 1,
            'username': username,
            'password': password,  # In production, use hashing!
            'created_at': datetime.now().isoformat()
        }
        users.append(user)
        save_json(USERS_FILE, users)
        return {'success': True, 'user': user}
    
    @staticmethod
    def authenticate(username, password):
        user = UserService.get_user(username)
        if user and user['password'] == password:
            return {'success': True, 'user': user}
        return {'success': False, 'message': 'Invalid credentials'}

