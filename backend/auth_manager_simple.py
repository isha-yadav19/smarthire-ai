"""
SmartHire.AI - Simple Authentication Module
File-based authentication without PostgreSQL dependency
"""

import bcrypt
import json
from pathlib import Path
from datetime import datetime

class AuthManager:
    def __init__(self):
        """Initialize with JSON file storage"""
        self.users_file = Path(__file__).parent.parent / 'data' / 'users.json'
        self.users_file.parent.mkdir(exist_ok=True)
        self.users = self._load_users()
    
    def _load_users(self):
        """Load users from JSON file"""
        if self.users_file.exists():
            with open(self.users_file, 'r') as f:
                data = json.load(f)
                # Handle both formats: {"users": [...]} and {"username": {...}}
                if isinstance(data, dict) and "users" in data:
                    # Convert array format to dict format
                    users_dict = {}
                    for user in data["users"]:
                        users_dict[user['username']] = user
                    return users_dict
                elif isinstance(data, dict):
                    return data
                else:
                    return self._create_default_users()
        else:
            return self._create_default_users()
    
    def _create_default_users(self):
        """Create default users"""
        default_users = {
            "admin": {
                "id": 1,
                "username": "admin",
                "email": "admin@smarthire.ai",
                "password_hash": self.hash_password("admin123"),
                "role": "admin",
                "is_active": True,
                "created_at": datetime.now().isoformat()
            },
            "recruiter": {
                "id": 2,
                "username": "recruiter",
                "email": "recruiter@company.com",
                "password_hash": self.hash_password("recruiter123"),
                "role": "recruiter",
                "is_active": True,
                "created_at": datetime.now().isoformat()
            },
            "candidate": {
                "id": 3,
                "username": "candidate",
                "email": "candidate@email.com",
                "password_hash": self.hash_password("candidate123"),
                "role": "candidate",
                "is_active": True,
                "created_at": datetime.now().isoformat()
            }
        }
        self._save_users(default_users)
        return default_users
    
    def _save_users(self, users):
        """Save users to JSON file"""
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)
    
    def hash_password(self, password):
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password, hashed_password):
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    def login(self, username, password):
        """Authenticate user"""
        try:
            username = username.strip()
            # Find user by username or email
            user = None
            for u in self.users.values():
                # Handle missing is_active field
                if 'is_active' not in u:
                    u['is_active'] = True
                
            if u['username'].lower() == username.lower() or u['email'].lower() == username.lower():
                    user = u
                    break
            
            if not user:
                return {"success": False, "message": "User not found"}
            
            if not user.get('is_active', True):
                return {"success": False, "message": "Account is inactive"}
            
            if self.verify_password(password, user['password_hash']):
                # Update last login
                user['last_login'] = datetime.now().isoformat()
                self._save_users(self.users)
                
                return {
                    "success": True,
                    "user": {
                        "id": user['id'],
                        "username": user['username'],
                        "email": user['email'],
                        "role": user['role']
                    }
                }
            else:
                return {"success": False, "message": "Invalid password"}
        
        except Exception as e:
            return {"success": False, "message": f"Login error: {str(e)}"}
    
    def register_user(self, username, email, password, role='recruiter'):
        """Register new user"""
        try:
            # Trim whitespace to prevent duplicate accounts
            username = username.strip()
            email = email.strip()

            # Check if user exists
            for u in self.users.values():
                if u['username'] == username:
                    return {"success": False, "message": "Username already exists"}
                if u['email'] == email:
                    return {"success": False, "message": "Email already exists"}
            
            # Create new user
            user_id = max([u['id'] for u in self.users.values()]) + 1
            new_user = {
                "id": user_id,
                "username": username,
                "email": email,
                "password_hash": self.hash_password(password),
                "role": role,
                "is_active": True,
                "created_at": datetime.now().isoformat()
            }
            
            self.users[username] = new_user
            self._save_users(self.users)
            
            return {
                "success": True,
                "message": "User registered successfully",
                "user_id": user_id
            }
        
        except Exception as e:
            return {"success": False, "message": f"Registration error: {str(e)}"}
    
    def get_user_by_id(self, user_id):
        """Get user details by ID"""
        for user in self.users.values():
            if user['id'] == user_id:
                return {
                    "id": user['id'],
                    "username": user['username'],
                    "email": user['email'],
                    "role": user['role']
                }
        return None
    
    def close(self):
        """Placeholder for compatibility"""
        pass


# Test authentication
if __name__ == "__main__":
    auth = AuthManager()
    
    print("=" * 60)
    print("Testing Simple Authentication System")
    print("=" * 60)
    
    print("\n[*] Default Users:")
    for user in auth.users.values():
        print(f"  - {user['username']} ({user['role']}) - {user['email']}")
    
    print("\n[*] Testing Logins:")
    
    print("\n1. Admin Login:")
    result = auth.login('admin', 'admin123')
    print(f"   [{'OK' if result['success'] else 'FAIL'}] {result.get('message', 'Success')}")
    
    print("\n2. Recruiter Login:")
    result = auth.login('recruiter', 'recruiter123')
    print(f"   [{'OK' if result['success'] else 'FAIL'}] {result.get('message', 'Success')}")
    
    print("\n3. Candidate Login:")
    result = auth.login('candidate', 'candidate123')
    print(f"   [{'OK' if result['success'] else 'FAIL'}] {result.get('message', 'Success')}")
    
    print("\n4. Wrong Password:")
    result = auth.login('admin', 'wrongpassword')
    print(f"   [{'OK' if result['success'] else 'FAIL'}] {result['message']}")
    
    print("\n5. Non-existent User:")
    result = auth.login('nonexistent', 'password')
    print(f"   [{'OK' if result['success'] else 'FAIL'}] {result['message']}")
    
    print("\n" + "=" * 60)
