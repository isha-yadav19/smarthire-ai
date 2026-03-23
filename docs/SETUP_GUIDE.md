# SmartHire.AI - Complete Setup Guide

## 📁 Clean Project Structure

```
Resume_Parser_Project/
├── auth/
│   └── login.html              # Modern login page (all-in-one)
│
├── data/
│   ├── config.json             # Scoring weights
│   ├── skills_taxonomy.json    # Skills database
│   ├── users.json              # User accounts
│   ├── jobs.json               # Job postings
│   ├── applications.json       # Applications
│   └── courses.json            # Course recommendations
│
├── extractors/
│   ├── keyword_extractor.py    # Skills & keyword extraction
│   ├── ats_scorer.py           # ATS scoring
│   └── skill_gap_analyzer.py   # Skill gap analysis
│
├── matcher/
│   └── scorer.py               # Candidate scoring & ranking
│
├── parsers/
│   ├── resume_parser.py        # PDF/DOCX parsing
│   └── jd_parser.py            # Job description parsing
│
├── input/                      # 500 sample resumes
│
├── Core Files:
│   ├── app.py                  # Main Streamlit app
│   ├── api_server.py           # Flask API backend
│   ├── auth_manager_simple.py  # File-based authentication
│   ├── screen.py               # Screening logic
│   └── main.py                 # CLI interface
│
├── Helper Scripts:
│   ├── start_api.bat           # Start API server
│   ├── start_login.bat         # Start login page server
│   └── start_login_server.py   # Login page HTTP server
│
└── Documentation:
    ├── README.md               # Main documentation
    ├── LOGIN_QUICKSTART.md     # Login setup guide
    ├── QUICK_START.md          # Quick start guide
    └── RUN_INSTRUCTIONS.md     # Running instructions
```

## 🚀 How to Run Everything

### Option 1: Complete System (Recommended)

**Terminal 1 - API Server:**
```bash
python api_server.py
```
Running on: http://localhost:5000

**Terminal 2 - Login Page:**
```bash
python start_login_server.py
```
Running on: http://localhost:8000

**Terminal 3 - Streamlit App:**
```bash
streamlit run app.py
```
Running on: http://localhost:8501

**Access:**
1. Open browser: http://localhost:8000/login.html
2. Login with your credentials
3. Redirects to Streamlit app

---

### Option 2: Direct Streamlit (No Login)

```bash
streamlit run app.py
```
Open: http://localhost:8501

---

### Option 3: CLI Mode

```bash
python main.py
```
Processes resumes from `input/` folder

---

## 👥 User Accounts

Your existing users from `data/users.json`:

### Candidates
- isha yadav (yadavisha9211@gmail.com)
- isha (Ishayadav1291@gmail.com)
- kirti (kirtinalwade123@gmail.com)

### Recruiters
- Adarsh (adarsh123@gmail.com)
- ada (ada123@dmail.com)

---

## 🔧 Quick Start Scripts

### Windows:
- `start_api.bat` - Start API server
- `start_login.bat` - Start login page

### Manual:
```bash
# API Server
python api_server.py

# Login Page
python start_login_server.py

# Streamlit App
streamlit run app.py
```

---

## 📊 Features

### Resume Processing
- ✅ PDF & DOCX parsing
- ✅ Batch processing (500+ resumes)
- ✅ Skills extraction (1000+ skills)
- ✅ Experience calculation
- ✅ Contact extraction

### Intelligent Matching
- ✅ Weighted scoring algorithm
- ✅ Required/preferred skills matching
- ✅ ATS compatibility scoring
- ✅ Skill gap analysis
- ✅ Course recommendations

### User Interface
- ✅ Modern login page
- ✅ Streamlit web app
- ✅ CLI interface
- ✅ REST API

### Export Options
- ✅ CSV export
- ✅ JSON export
- ✅ Individual resume downloads
- ✅ Bulk ZIP downloads

---

## 🛠️ Configuration

### Scoring Weights (`data/config.json`)
```json
{
  "weights": {
    "required_skills": 0.40,
    "preferred_skills": 0.20,
    "experience": 0.15,
    "keyword_density": 0.10,
    "ats_score": 0.05,
    "semantic_similarity": 0.10
  }
}
```

### Skills Database
- Location: `data/skills_taxonomy.json`
- 1000+ technical and soft skills
- Categorized by domain

---

## 📝 Workflow

1. **Login** → http://localhost:8000/login.html
2. **Upload Resumes** → Streamlit interface
3. **Enter Job Description** → Required/preferred skills
4. **Process** → Automatic scoring & ranking
5. **Review Results** → Sorted by match score
6. **Export** → CSV, JSON, or ZIP

---

## 🔒 Authentication

### File-Based (Current)
- No PostgreSQL required
- Uses `data/users.json`
- Bcrypt password hashing
- Session management

### PostgreSQL (Optional)
- Set up database
- Configure `.env` file
- System auto-switches

---

## 📦 Dependencies

```bash
pip install -r requirements.txt
```

Key packages:
- streamlit
- flask
- flask-cors
- bcrypt
- PyPDF2
- python-docx
- pandas

---

## 🎯 Next Steps

1. **Test Login**: Open http://localhost:8000/login.html
2. **Process Resumes**: Use sample resumes in `input/`
3. **Customize**: Edit scoring weights in `data/config.json`
4. **Add Skills**: Update `data/skills_taxonomy.json`

---

## 📞 Support

- Check `LOGIN_QUICKSTART.md` for login issues
- See `README.md` for detailed documentation
- Review `RUN_INSTRUCTIONS.md` for execution help

---

**Made with ❤️ for efficient recruitment**
