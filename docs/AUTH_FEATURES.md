# 🔐 Authentication Features - Complete Guide

## ✅ **Fully Implemented Features**

### 1. **Sign Up (Registration)** ✓
- **Page**: `auth/signup.html`
- **Features**:
  - Email/password registration
  - Role selection (Candidate/Recruiter)
  - Terms & conditions checkbox
  - Automatic account creation
  - Redirect to login after success

**How to use:**
1. Open: http://localhost:8000/signup.html
2. Select role (Candidate/Recruiter)
3. Enter name, email, password
4. Click "Create account"
5. Redirected to login page

---

### 2. **Sign In (Login)** ✓
- **Page**: `auth/login.html`
- **Features**:
  - Email/password authentication
  - Role-based login
  - "Remember me" option
  - Session management
  - Redirect to Streamlit app

**How to use:**
1. Open: http://localhost:8000/login.html
2. Select role (Candidate/Recruiter)
3. Enter email and password
4. Click "Sign in"
5. Redirected to http://localhost:8501

---

### 3. **Forgot Password (Reset)** ✓
- **Page**: `auth/forgot-password.html`
- **Features**:
  - Email-based password reset
  - Auto-generated secure password
  - Instant password display (demo mode)
  - Direct link to login

**How to use:**
1. Click "Forgot password?" on login page
2. Enter your email
3. Click "Send reset link"
4. New password displayed on screen
5. Copy password and sign in

**Note:** In production, password would be sent via email.

---

### 4. **Google OAuth** ⏳
- **Status**: Requires setup
- **Guide**: See `GOOGLE_OAUTH_SETUP.md`
- **Current**: Shows setup instructions

**To enable:**
1. Create Google Cloud project
2. Get OAuth credentials
3. Add Client ID to config
4. Restart servers

---

## 🚀 **Quick Start**

### **New User Flow:**
```
1. Open login page
2. Click "Sign up free"
3. Fill registration form
4. Create account
5. Redirected to login
6. Sign in with new credentials
7. Access Streamlit app
```

### **Existing User Flow:**
```
1. Open login page
2. Enter email/password
3. Sign in
4. Access Streamlit app
```

### **Forgot Password Flow:**
```
1. Click "Forgot password?"
2. Enter email
3. Get new password
4. Sign in with new password
```

---

## 📁 **File Structure**

```
auth/
├── login.html              # Sign in page
├── signup.html             # Registration page
├── forgot-password.html    # Password reset page
└── google_config.json      # OAuth config (create this)
```

---

## 🔧 **API Endpoints**

### **POST /api/login**
Login with email/password
```json
{
  "username": "email@example.com",
  "password": "password123",
  "role": "recruiter"
}
```

### **POST /api/register**
Create new account
```json
{
  "username": "John Doe",
  "email": "email@example.com",
  "password": "password123",
  "role": "recruiter"
}
```

### **POST /api/reset-password**
Reset forgotten password
```json
{
  "email": "email@example.com"
}
```

### **POST /api/logout**
End user session

### **GET /api/check-session**
Verify login status

---

## 🎯 **Testing**

### **Test Sign Up:**
```bash
# 1. Start API server
python api_server.py

# 2. Start login server
python start_login_server.py

# 3. Open browser
http://localhost:8000/signup.html

# 4. Create account
Name: Test User
Email: test@example.com
Password: test123
Role: Recruiter

# 5. Verify in data/users.json
```

### **Test Login:**
```bash
# Use existing account
Email: adarsh123@gmail.com
Password: (your password)
Role: Recruiter
```

### **Test Password Reset:**
```bash
# 1. Go to forgot password page
http://localhost:8000/forgot-password.html

# 2. Enter email
Email: test@example.com

# 3. Copy new password
# 4. Login with new password
```

---

## 🔒 **Security Features**

✅ **Bcrypt password hashing**
✅ **Session management**
✅ **CORS protection**
✅ **Input validation**
✅ **SQL injection prevention** (using JSON storage)
✅ **XSS protection** (input sanitization)

---

## 📊 **User Data Storage**

**Location**: `data/users.json`

**Format**:
```json
{
  "username": {
    "id": 1,
    "username": "John Doe",
    "email": "john@example.com",
    "password_hash": "$2b$12$...",
    "role": "recruiter",
    "is_active": true,
    "created_at": "2026-03-22T...",
    "last_login": "2026-03-22T..."
  }
}
```

---

## 🎨 **UI Features**

✅ Modern techy design
✅ Smooth animations
✅ Responsive layout
✅ Error messages
✅ Success notifications
✅ Loading states
✅ Form validation
✅ Tab switching
✅ Mobile-friendly

---

## 🐛 **Troubleshooting**

### **"Connection error" message**
- ✓ Make sure API server is running: `python api_server.py`
- ✓ Check port 5000 is not in use

### **"User not found"**
- ✓ Check email spelling
- ✓ Verify account exists in `data/users.json`

### **"Invalid password"**
- ✓ Use correct password
- ✓ Try password reset if forgotten

### **Can't access pages**
- ✓ Start login server: `python start_login_server.py`
- ✓ Or use: `open_login.bat`

---

## 🚀 **Next Steps**

1. ✅ **Sign Up** - Working
2. ✅ **Login** - Working
3. ✅ **Password Reset** - Working
4. ⏳ **Google OAuth** - Requires setup
5. 🔜 **Email verification** - Future
6. 🔜 **Two-factor auth** - Future
7. 🔜 **Social login (GitHub, LinkedIn)** - Future

---

## 📞 **Support**

- **Setup issues**: See `SETUP_GUIDE.md`
- **Google OAuth**: See `GOOGLE_OAUTH_SETUP.md`
- **API docs**: See `api_server.py` comments
- **Login issues**: See `LOGIN_QUICKSTART.md`

---

**All authentication features are now fully functional!** 🎉
