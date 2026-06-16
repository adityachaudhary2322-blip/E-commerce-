"""
User Management Module - Handles user registration, login, profile management
"""

from datetime import datetime
import uuid

class UserManager:
    """Manages all user operations"""
    
    def __init__(self, storage):
        self.storage = storage
    
    def register(self, name, email, password):
        """Register a new user"""
        # Check if email already exists
        users = self.storage.load_users()
        
        for user in users:
            if user['email'] == email:
                return None
        
        # Create new user
        user_id = str(uuid.uuid4())[:8]
        new_user = {
            'user_id': user_id,
            'name': name,
            'email': email,
            'password': password,
            'registered_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'order_history': []
        }
        
        users.append(new_user)
        self.storage.save_users(users)
        return user_id
    
    def login(self, email, password):
        """Login user"""
        users = self.storage.load_users()
        
        for user in users:
            if user['email'] == email and user['password'] == password:
                return user
        return None
    
    def update_password(self, email, old_password, new_password):
        """Update user password"""
        users = self.storage.load_users()
        
        for user in users:
            if user['email'] == email and user['password'] == old_password:
                user['password'] = new_password
                self.storage.save_users(users)
                return True
        return False
    
    def get_user(self, user_id):
        """Get user by ID"""
        users = self.storage.load_users()
        
        for user in users:
            if user['user_id'] == user_id:
                return user
        return None