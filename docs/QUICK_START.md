# Resume Screening System - Quick Start Guide

## ✅ How to Use This Project

**YOU upload:**
1. Your resumes (PDF, DOCX, or TXT format)
2. Your job description (PDF, DOCX, or TXT format)

**YOU get:**
- Top N best matching resumes (you choose N: 5, 10, 20, 100, etc.)
- Match scores for each resume
- CSV file you can open in Excel

---

## 🚀 Simple 3-Step Process

### **Step 1:** Put ALL your files in the `input` folder

```
input/
├── job_description.pdf                 ← Your JD (PDF, DOCX, or TXT)
├── john_smith_resume.pdf               ← Your resumes
├── sarah_johnson_resume.docx           ← (PDF, DOCX, or TXT)
├── mike_chen_resume.txt
└── ... (put all your resume files here)
```

**Important:** Your JD filename should contain one of these words: `job`, `jd`, `description`, or `position`

### **Step 2:** Run ONE command

```bash
python screen.py --folder input --top 10
```

Change `10` to how many top matches you want (5, 10, 20, 100, etc.)

### **Step 3:** Open results

Results saved in `output/` folder as CSV file → Open in Excel!

---

## 📋 Real Examples

```bash
# Get top 10 matches
python screen.py --folder input --top 10

# Get top 5 matches
python screen.py --folder input --top 5

# Get top 20 matches
python screen.py --folder input --top 20

# Get top 15 with minimum 70% score
python screen.py --folder input --top 15 --min-score 70

# Output as JSON instead of CSV
python screen.py --folder input --top 10 --format json
```

---

## 📁 Supported File Formats

**Resumes:** PDF, DOCX, DOC, TXT  
**Job Description:** PDF, DOCX, DOC, TXT

**All formats work together!** You can mix PDF resumes with DOCX resumes in the same folder.

---

## 📊 What You Get in Results

### CSV Output (opens in Excel)
Location: `output/results_*.csv`

**Columns:**
- **Rank**: 1, 2, 3... (sorted by best match)
- **Name**: Candidate name
- **Total Score**: Match percentage (0-100%)
- **Required Skills**: How many required skills matched
- **Preferred Skills**: How many preferred skills matched
- **Experience**: Experience match score
- **Matched Skills**: List of skills found in resume
- **Missing Skills**: Required skills not found

---

## 💡 Tips for Best Results

### Job Description Format

**Good JD Format:**
```
Senior Java Developer

Required Skills:
- 5+ years of Java development experience
- Spring Boot, Hibernate
- MySQL, PostgreSQL
- REST APIs
- Git, Maven

Preferred Skills:
- AWS or Azure
- Docker, Kubernetes
- Microservices
- Angular or React
```

**What the System Extracts:**
- Keywords like "Required", "Must have", "Mandatory" → Required Skills
- Keywords like "Preferred", "Nice to have", "Desired" → Preferred Skills
- "5+ years", "minimum 3 years" → Experience requirements
- Technology names → Keywords for matching

### Scoring Weights

Default weights (can change in `data/config.json`):
- Required Skills: **50%** (most important)
- Preferred Skills: **25%**
- Experience Match: **15%**
- Keyword Density: **10%**

---

## 🎯 That's It!

**Your workflow:**
1. Add your files to `input/` folder
2. Run: `python screen.py --folder input --top 10`
3. Open CSV file in `output/` folder with Excel

**Done!** 🚀
