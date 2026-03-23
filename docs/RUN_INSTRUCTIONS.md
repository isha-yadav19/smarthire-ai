# SmartHire.AI - Complete Setup Guide

## 🚀 Quick Start (5 Steps)

### **Step 1: Install PostgreSQL**

**Windows:**
1. Download: https://www.postgresql.org/download/windows/
2. Run installer
3. Set password for 'postgres' user (remember this!)
4. Default port: 5432
5. Install pgAdmin 4 (included)

**Verify Installation:**
```bash
psql --version
```

---

### **Step 2: Create Database**

**Option A: Using pgAdmin 4**
1. Open pgAdmin 4
2. Right-click "Databases" → Create → Database
3. Name: `smarthire_db`
4. Click Save

**Option B: Using Command Line**
```bash
psql -U postgres
CREATE DATABASE smarthire_db;
\q
```

---

### **Step 3: Run Database Schema**

**Option A: Using pgAdmin 4**
1. Open pgAdmin 4
2. Connect to `smarthire_db`
3. Click "Query Tool"
4. Open file: `schema.sql`
5. Click "Execute" (F5)

**Option B: Using Command Line**
```bash
psql -U postgres -d smarthire_db -f schema.sql
```

**Expected Output:**
```
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
INSERT 0 2
```

---

### **Step 4: Configure Environment**

Edit `.env` file with your PostgreSQL password:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=smarthire_db
DB_USER=postgres
DB_PASSWORD=YOUR_PASSWORD_HERE  # Change this!
```

---

### **Step 5: Install Python Dependencies**

```bash
# Activate virtual environment (if using)
# Windows:
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🎯 Running the System

### **You need 2 terminals running simultaneously:**

### **Terminal 1: Backend API Server**
```bash
python api_server.py
```

**Expected Output:**
```
============================================================
SmartHire.AI Backend Server
============================================================
Server running on: http://localhost:5000
API Endpoints:
  POST /api/login       - User login
  POST /api/logout      - User logout
  GET  /api/check-session - Check login status
  POST /api/register    - Register user (admin only)
  GET  /health          - Health check
============================================================
 * Running on http://0.0.0.0:5000
```

---

### **Terminal 2: Streamlit Dashboard**
```bash
streamlit run dashboard.py
```

**Expected Output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

---

## 🔐 Access the System

### **Step 1: Open Login Page**
```
http://localhost:5000/auth/login.html
```

Or directly open: `Resume_Parser_Project/auth/login.html`

### **Step 2: Login with Demo Accounts**

**Admin Account:**
- Email: `admin@smarthire.ai`
- Password: `password123`

**Recruiter Account:**
- Email: `recruiter1@smarthire.ai`
- Password: `password123`

### **Step 3: Access Dashboard**
After login, you'll be redirected to:
```
http://localhost:8501
```

---

## 🧪 Testing the System

### **Test 1: Database Connection**
```bash
python db_connection.py
```

**Expected:**
```
✅ Database connected successfully!
Testing database connection...
Found 2 users in database
  - admin (admin)
  - recruiter1 (recruiter)
Database connection closed
```

---

### **Test 2: Authentication**
```bash
python auth_manager.py
```

**Expected:**
```
Testing Authentication System...
--------------------------------------------------

1. Testing Admin Login:
   Result: {'success': True, 'user': {...}}

2. Testing Recruiter Login:
   Result: {'success': True, 'user': {...}}

3. Testing Wrong Password:
   Result: {'success': False, 'message': 'Invalid password'}

4. Testing Non-existent User:
   Result: {'success': False, 'message': 'User not found'}
```

---

### **Test 3: API Health Check**
Open browser:
```
http://localhost:5000/health
```

**Expected:**
```json
{
  "status": "healthy",
  "service": "SmartHire.AI API"
}
```

---

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    USER BROWSER                         │
└─────────────────────────────────────────────────────────┘
                          │
                          ↓
┌─────────────────────────────────────────────────────────┐
│              login.html (Port: File System)             │
│              - Corporate login page                     │
│              - Role selection                           │
│              - Form validation                          │
└─────────────────────────────────────────────────────────┘
                          │
                          ↓ (POST /api/login)
┌─────────────────────────────────────────────────────────┐
│           Flask API Server (Port: 5000)                 │
│           - api_server.py                               │
│           - Authentication endpoints                    │
│           - Session management                          │
└─────────────────────────────────────────────────────────┘
                          │
                          ↓
┌─────────────────────────────────────────────────────────┐
│           Authentication Layer                          │
│           - auth_manager.py                             │
│           - Password hashing (bcrypt)                   │
│           - User verification                           │
└─────────────────────────────────────────────────────────┘
                          │
                          ↓
┌─────────────────────────────────────────────────────────┐
│           PostgreSQL Database                           │
│           - smarthire_db                                │
│           - 5 tables (users, candidates, jobs, etc.)    │
└─────────────────────────────────────────────────────────┘
                          │
                          ↑
┌─────────────────────────────────────────────────────────┐
│        Streamlit Dashboard (Port: 8501)                 │
│        - dashboard.py                                   │
│        - Role-based views (Admin/Recruiter)             │
│        - Resume upload & screening                      │
└─────────────────────────────────────────────────────────┘
```

---

## 🎭 User Roles & Permissions

### **Admin**
✅ View all users
✅ Create new users
✅ View all candidates
✅ View all job postings
✅ System configuration
✅ Analytics dashboard

### **Recruiter**
✅ Upload resumes
✅ View all candidates
✅ Create job postings
✅ Screen candidates
✅ View screening results
❌ User management
❌ System configuration

---

## 🐛 Troubleshooting

### **Issue: Database connection failed**
```
Error: psycopg2.OperationalError: could not connect to server
```

**Solution:**
1. Check PostgreSQL is running
2. Verify password in `.env` file
3. Test connection: `psql -U postgres -d smarthire_db`

---

### **Issue: Backend server won't start**
```
Error: Address already in use
```

**Solution:**
```bash
# Windows: Kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Then restart
python api_server.py
```

---

### **Issue: Login page can't connect to backend**
```
Connection error in browser console
```

**Solution:**
1. Make sure `api_server.py` is running
2. Check: http://localhost:5000/health
3. Check browser console for CORS errors

---

### **Issue: Streamlit shows "Please login first"**
```
Warning: Please login first
```

**Solution:**
1. Use the demo login in sidebar (temporary)
2. Or integrate with Flask session (production)

---

## 📁 Project Structure

```
Resume_Parser_Project/
├── auth/
│   ├── login.html          # Corporate login page
│   ├── login.css           # Styling
│   └── login.js            # Frontend logic
├── parsers/
│   ├── resume_parser.py    # PDF/DOCX parsing
│   └── jd_parser.py        # Job description parsing
├── extractors/
│   └── keyword_extractor.py # Skills extraction
├── matcher/
│   └── scorer.py           # Scoring algorithm
├── data/
│   ├── config.json         # Scoring weights
│   └── skills_taxonomy.json # Skills database
├── api_server.py           # Flask backend API
├── auth_manager.py         # Authentication logic
├── db_connection.py        # Database connection
├── dashboard.py            # Streamlit dashboard (NEW)
├── app.py                  # Original Streamlit app
├── schema.sql              # Database schema
├── .env                    # Environment variables
├── requirements.txt        # Python dependencies
└── RUN_INSTRUCTIONS.md     # This file
```

---

## 🎯 Demo Flow

### **Complete Demo (2 minutes):**

1. **Start servers** (2 terminals)
   ```bash
   python api_server.py
   streamlit run dashboard.py
   ```

2. **Open login page**
   - Navigate to: `auth/login.html`
   - Select role: Admin
   - Email: admin@smarthire.ai
   - Password: password123
   - Click "Sign In"

3. **Admin Dashboard**
   - View metrics (users, candidates, jobs)
   - Create new recruiter user
   - View system configuration

4. **Logout and login as Recruiter**
   - Email: recruiter1@smarthire.ai
   - Password: password123

5. **Recruiter Dashboard**
   - Upload resumes
   - Create job posting
   - Screen candidates
   - View results

---

## 📝 Next Steps

### **To Complete Integration:**

1. **Connect resume upload to database**
   - Integrate `resume_parser.py` with dashboard
   - Save parsed data to `candidates` table

2. **Connect screening to database**
   - Integrate `scorer.py` with dashboard
   - Save results to `screening_results` table

3. **Add learning recommendations**
   - Implement skill gap analysis
   - Save to `learning_recommendations` table

4. **Add ATS scoring**
   - Implement ATS checker
   - Add to scoring algorithm

5. **Add NLP semantic matching**
   - Integrate sentence transformers
   - Add semantic similarity score

---

## 🎓 For College Project

### **What to Demonstrate:**

1. ✅ **Login System** - Corporate design, role-based
2. ✅ **Database** - PostgreSQL with 5 tables
3. ✅ **Authentication** - Bcrypt password hashing
4. ✅ **API Backend** - Flask REST API
5. ✅ **Dashboard** - Role-based Streamlit UI
6. ✅ **CRUD Operations** - Create users, jobs, candidates
7. ⏳ **Resume Parsing** - PDF/DOCX extraction
8. ⏳ **Scoring Algorithm** - Weighted matching
9. ⏳ **Analytics** - Charts and metrics

### **Documentation to Prepare:**

- ER Diagram (database schema)
- Architecture diagram (shown above)
- API documentation
- User manual
- Screenshots of each feature

---

## 🚀 You're Ready!

**Start the system:**
```bash
# Terminal 1
python api_server.py

# Terminal 2
streamlit run dashboard.py

# Browser
Open: auth/login.html
```

**Good luck with your project!** 🎯
