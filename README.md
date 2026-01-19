# Resume Screening System

An intelligent, automated resume screening system that processes hundreds of resumes against job descriptions and ranks candidates based on skills match, experience, and relevance.

## Features

- **Batch Processing**: Process 500-1000 resumes simultaneously
- **Multi-Format Support**: Parse PDF and DOCX resumes automatically
- **Intelligent Matching**: Weighted scoring algorithm for accurate candidate ranking
- **Skills Taxonomy**: Comprehensive skills database with 1000+ technical and soft skills
- **Web Interface**: User-friendly Streamlit UI for easy interaction
- **Export Options**: Download results as CSV, JSON, or bulk ZIP of top resumes
- **Individual Downloads**: Access each candidate's resume directly from results
- **Contact Extraction**: Automatic extraction of names, emails, and phone numbers

## Architecture

```
Resume_Parser_Project/
├── app.py                  # Streamlit web interface
├── main.py                 # CLI-based processing script
├── screen.py               # Screening logic
├── parsers/
│   ├── resume_parser.py    # Resume text extraction (PDF/DOCX)
│   └── jd_parser.py        # Job description parsing
├── extractors/
│   └── keyword_extractor.py # Skills, experience, keyword extraction
├── matcher/
│   └── scorer.py           # Scoring and ranking algorithm
├── data/
│   ├── config.json         # Scoring weights configuration
│   └── skills_taxonomy.json # Skills database
├── input/                  # Input folder for resumes and JD
├── output/                 # Results storage
└── requirements.txt        # Python dependencies
```

## Scoring Algorithm

The system uses a weighted scoring approach:

- **50%**: Required Skills Match
- **25%**: Preferred Skills Match
- **15%**: Years of Experience
- **10%**: Keyword Relevance

You can customize these weights in [data/config.json](data/config.json).

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Git (for cloning)

### Setup Steps

1. **Clone the repository**
```bash
git clone https://github.com/abdultalha0862/Resume_Parser_Project.git
cd Resume_Parser_Project
```

2. **Create virtual environment**
```bash
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

## Usage

### Web Interface (Recommended)

1. **Start the Streamlit app**
```bash
streamlit run app.py
```

2. **Access the interface**
- Open your browser to `http://localhost:8501`

3. **Process resumes**
- Enter job description in the text area
- Upload resume files (PDF or DOCX)
- Click "Process Resumes"
- View ranked results with scores
- Download individual resumes or export all results

### Command Line Interface

1. **Prepare input files**
- Place resumes in `input/` folder
- Create `input/job_description.txt` with job requirements

2. **Run the screening**
```bash
python main.py
```

3. **View results**
- Results saved to `output/` folder as CSV
- Timestamped filename: `results_job_description_YYYYMMDD_HHMMSS.csv`

## Configuration

### Scoring Weights

Edit [data/config.json](data/config.json) to customize scoring:

```json
{
  "weights": {
    "required_skills": 0.50,
    "preferred_skills": 0.25,
    "experience": 0.15,
    "keywords": 0.10
  }
}
```

### Skills Taxonomy

The [data/skills_taxonomy.json](data/skills_taxonomy.json) contains 1000+ skills across categories:
- Programming Languages
- Frameworks & Libraries
- Databases
- Cloud Platforms
- DevOps Tools
- Soft Skills

Add custom skills to expand matching capabilities.

## Job Description Format

For optimal results, structure your job description with:

**Required Skills:**
- Python, JavaScript, SQL
- React, Node.js
- AWS, Docker

**Preferred Skills:**
- Kubernetes, Terraform
- CI/CD, Jenkins

**Experience:**
- 3+ years in software development

**Keywords:**
- Agile, Scrum, REST APIs

## Output Format

### CSV Results

| Rank | Filename | Name | Email | Phone | Score | Required Skills | Preferred Skills | Experience | Keywords |
|------|----------|------|-------|-------|-------|----------------|------------------|------------|----------|
| 1 | REAL_0042_Grant_Smith.pdf | Grant Smith | grant@email.com | (555) 123-4567 | 92.5 | Python, AWS, React | Kubernetes | 5 years | Agile, CI/CD |

### JSON Export

```json
{
  "rank": 1,
  "filename": "REAL_0042_Grant_Smith.pdf",
  "name": "Grant Smith",
  "email": "grant@email.com",
  "phone": "(555) 123-4567",
  "total_score": 92.5,
  "required_skills_score": 48.5,
  "preferred_skills_score": 22.0,
  "experience_score": 15.0,
  "keywords_score": 7.0
}
```

## Deployment

### Streamlit Cloud (Free)

1. Push code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Select `app.py` as the main file
5. Deploy (auto-updates on push)

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

### Local Network Deployment

```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

Access from other devices: `http://<your-ip>:8501`

## Troubleshooting

### Import Errors

```bash
# Ensure virtual environment is activated
# Windows
.\venv\Scripts\Activate.ps1

# Install dependencies again
pip install -r requirements.txt
```

### PDF Parsing Issues

- Ensure PyPDF2 is installed: `pip install PyPDF2>=3.0.1`
- Some encrypted PDFs may not parse correctly
- Try converting PDFs to DOCX format

### Memory Issues (Large Batches)

- Process resumes in smaller batches (100-200 at a time)
- Increase Streamlit upload limit in `.streamlit/config.toml`
- Close other applications to free memory

## Technologies Used

- **Python 3.8+**: Core language
- **Streamlit**: Web interface framework
- **PyPDF2**: PDF text extraction
- **python-docx**: DOCX parsing
- **Pandas**: Data manipulation and export
- **ReportLab**: PDF generation (future feature)

## Project Structure Details

### Parsers Module

- `resume_parser.py`: Extracts text from PDF/DOCX files
- `jd_parser.py`: Parses structured job descriptions

### Extractors Module

- `keyword_extractor.py`: 
  - Skills extraction using taxonomy matching
  - Experience calculation from dates
  - Keyword frequency analysis
  - Contact information extraction

### Matcher Module

- `scorer.py`:
  - Calculates weighted scores
  - Ranks candidates by total score
  - Generates match percentages

## Performance

- **Processing Speed**: ~2-5 resumes/second
- **Batch Size**: Up to 1000 resumes (memory dependent)
- **Accuracy**: 85-90% skill matching accuracy
- **Upload Limit**: 500MB (configurable)

## Future Enhancements

- [ ] Machine learning-based matching
- [ ] ATS keyword optimization
- [ ] Interview scheduling integration
- [ ] Email notification system
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Resume quality scoring

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit changes (`git commit -m 'Add YourFeature'`)
4. Push to branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Author

**Abdul Talha**
- GitHub: [@abdultalha0862](https://github.com/abdultalha0862)

## Acknowledgments

- Skills taxonomy inspired by industry standards
- Built with Python and Streamlit community tools
- Designed for HR professionals and recruitment teams

## Support

For issues, questions, or feature requests:
- Open an issue on [GitHub Issues](https://github.com/abdultalha0862/Resume_Parser_Project/issues)
- Email: [your-email@example.com]

---

**Made with ❤️ for efficient recruitment**
