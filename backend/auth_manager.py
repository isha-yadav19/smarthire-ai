"""
SmartHire.AI - Authentication Module
Handles user login, password verification, and session management
"""

import bcrypt
import json
from db_connection import Database

class AuthManager:
    def __init__(self):
        self.db = Database()
    
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
            user = self.db.get_user_by_username(username)
            
            if not user:
                return {"success": False, "message": "User not found"}
            
            if not user['is_active']:
                return {"success": False, "message": "Account is inactive"}
            
            if self.verify_password(password, user['password_hash']):
                # Update last login
                self.db.execute_query(
                    "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = %s",
                    (user['id'],),
                    fetch=False
                )
                
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
            # Check if user exists
            existing = self.db.get_user_by_username(username)
            if existing:
                return {"success": False, "message": "Username already exists"}
            
            # Hash password
            password_hash = self.hash_password(password)
            
            # Insert user
            user_id = self.db.insert_user(username, email, password_hash, role)
            
            if user_id:
                return {
                    "success": True,
                    "message": "User registered successfully",
                    "user_id": user_id
                }
            else:
                return {"success": False, "message": "Registration failed"}
        
        except Exception as e:
            return {"success": False, "message": f"Registration error: {str(e)}"}
    
    def get_user_by_id(self, user_id):
        """Get user details by ID"""
        query = "SELECT id, username, email, role FROM users WHERE id = %s"
        result = self.db.execute_query(query, (user_id,))
        return result[0] if result else None
    
    def close(self):
        """Close database connection"""
        self.db.close()


# Test authentication
if __name__ == "__main__":
    auth = AuthManager()
    
    print("Testing Authentication System...")
    print("-" * 50)
    
    # Test login with demo accounts
    print("\n1. Testing Admin Login:")
    result = auth.login('admin', 'password123')
    print(f"   Result: {result}")
    
    print("\n2. Testing Recruiter Login:")
    result = auth.login('recruiter1', 'password123')
    print(f"   Result: {result}")
    
    print("\n3. Testing Wrong Password:")
    result = auth.login('admin', 'wrongpassword')
    print(f"   Result: {result}")
    
    print("\n4. Testing Non-existent User:")
    result = auth.login('nonexistent', 'password')
    print(f"   Result: {result}")
    
    auth.close()
