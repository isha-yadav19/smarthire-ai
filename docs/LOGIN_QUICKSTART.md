# Quick Start - Login System (No PostgreSQL Required)

## Your Existing User Accounts

The system has loaded your existing users from `data/users.json`:

### Candidate Accounts
1. **isha yadav**
   - Email: yadavisha9211@gmail.com
   - Password: (your password)
   - Role: Candidate

2. **isha**
   - Email: Ishayadav1291@gmail.com
   - Password: (your password)
   - Role: Candidate

3. **kirti**
   - Email: kirtinalwade123@gmail.com
   - Password: (your password)
   - Role: Candidate

### Recruiter Accounts
1. **Adarsh**
   - Email: adarsh123@gmail.com
   - Password: (your password)
   - Role: Recruiter

2. **ada**
   - Email: ada123@dmail.com
   - Password: (your password)
   - Role: Recruiter

## How to Run

### 1. Start the Backend API Server

```bash
python api_server.py
```

You should see:
```
[OK] Using simple file-based authentication (no PostgreSQL required)
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
```

### 2. Open the Login Page

Open `auth/login.html` in your web browser:
- Right-click the file → Open with → Your browser
- Or navigate to: `file:///C:/Users/PC/OneDrive/Desktop/smarthire_1/Resume_Parser_Project/auth/login.html`

### 3. Login

1. Select your role (Candidate/Recruiter)
2. Enter email and password from the credentials above
3. Click "Sign in"
4. On success, you'll be redirected to the Streamlit app

## User Data Storage

User data is stored in: `data/users.json`

This file is automatically created with default users on first run.

## Troubleshooting

### "Connection error" message
- Make sure the API server is running (`python api_server.py`)
- Check that it's running on port 5000

### Login fails
- Verify you're using the correct credentials
- Check the role matches (Candidate/Recruiter)
- Look at the API server console for error messages

### Can't access Streamlit after login
- Start Streamlit: `streamlit run app.py`
- It should run on http://localhost:8501

## Adding New Users

You can add users by editing `data/users.json` or using the registration endpoint (admin only).

## Switching to PostgreSQL

To use PostgreSQL instead:
1. Install and start PostgreSQL
2. Configure `.env` file with database credentials
3. Run database setup: `python db_connection.py`
4. The system will automatically use PostgreSQL if available
