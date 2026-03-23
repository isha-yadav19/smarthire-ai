# Project Structure

## Directory Organization

```
Resume_Parser_Project/
├── parsers/              # Resume and job description parsing
├── extractors/           # Information extraction modules
├── matcher/              # Scoring and ranking logic
├── data/                 # Configuration and skills database
├── input/                # Input folder for resumes and JD
├── output/               # Results storage (generated)
├── auth/                 # Authentication UI components
├── .streamlit/           # Streamlit configuration
└── .amazonq/             # Amazon Q rules and memory bank
```

## Core Components

### Parsers Module (`parsers/`)
**Purpose**: Extract text from various resume formats and parse job descriptions

- `resume_parser.py`: PDF and DOCX text extraction
- `jd_parser.py`: Structured job description parsing
- `__init__.py`: Module initialization

**Responsibilities**:
- Handle multiple file formats (PDF, DOCX)
- Extract clean text from documents
- Parse job requirements into structured data
- Identify required/preferred skills sections

### Extractors Module (`extractors/`)
**Purpose**: Extract structured information from parsed text

- `keyword_extractor.py`: Skills, experience, and keyword extraction
- `ats_scorer.py`: ATS compatibility scoring
- `skill_gap_analyzer.py`: Identify missing skills and recommend courses
- `__init__.py`: Module initialization

**Responsibilities**:
- Match skills against taxonomy database
- Calculate years of experience from dates
- Extract contact information (name, email, phone)
- Analyze keyword frequency and density
- Score ATS compatibility
- Generate skill gap reports

### Matcher Module (`matcher/`)
**Purpose**: Score and rank candidates

- `scorer.py`: Weighted scoring algorithm and ranking
- `__init__.py`: Module initialization

**Responsibilities**:
- Calculate weighted scores across categories
- Rank candidates by total score
- Generate match percentages
- Apply configurable weights from config.json

### Data Module (`data/`)
**Purpose**: Configuration and reference data

- `config.json`: Scoring weights and system parameters
- `skills_taxonomy.json`: 1000+ skills database (programming, frameworks, tools, soft skills)
- `courses.json`: Course recommendations for skill gaps

**Configuration Structure**:
```json
{
  "weights": {
    "required_skills": 0.40,
    "preferred_skills": 0.20,
    "experience": 0.15,
    "keyword_density": 0.10,
    "ats_score": 0.05,
    "semantic_similarity": 0.10
  },
  "min_score": 0.0,
  "experience_tolerance": 2,
  "default_top_n": 10
}
```

### Authentication Module (`auth/`)
**Purpose**: User authentication UI

- `login.html`: Login page structure
- `login.css`: Login page styling
- `login.js`: Client-side authentication logic

## Entry Points

### Web Interface (`app.py`)
- Streamlit-based web UI
- File upload and job description input
- Real-time processing and results display
- Export and download functionality
- Primary user interface

### CLI Interface (`main.py`)
- Command-line batch processing
- Reads from `input/` folder
- Outputs to `output/` folder with timestamps
- Suitable for automation and scripting

### API Server (`api_server.py`)
- Flask-based REST API
- Endpoints for resume processing
- CORS-enabled for web integration
- Programmatic access to screening functionality

### Dashboard (`dashboard.py`)
- Analytics and visualization interface
- Candidate statistics and trends
- Database-backed reporting

## Supporting Files

### Database Layer
- `db_connection.py`: PostgreSQL connection management
- `schema.sql`: Database schema definition
- `.env`: Environment variables (database credentials)

### Authentication
- `auth_manager.py`: User authentication and session management
- Uses bcrypt for password hashing

### Utilities
- `screen.py`: Core screening logic orchestration
- `convert_to_pdf.py`: JSONL to PDF conversion utility
- `test_pdf_parsing.py`: PDF parsing validation
- `setup.py`: Project setup and initialization

### Documentation
- `README.md`: Comprehensive project documentation
- `DEPLOYMENT.md`: Deployment instructions
- `QUICK_START.md`: Quick start guide
- `RUN_INSTRUCTIONS.md`: Execution instructions
- `DATABASE_SETUP.md`: Database configuration guide

### Configuration
- `requirements.txt`: Python dependencies
- `.gitignore`: Git ignore patterns
- `.streamlit/config.toml`: Streamlit server configuration

## Data Flow

1. **Input**: Resumes (PDF/DOCX) + Job Description
2. **Parsing**: Extract text from documents
3. **Extraction**: Identify skills, experience, keywords, contacts
4. **Matching**: Score against job requirements
5. **Ranking**: Sort candidates by weighted score
6. **Output**: CSV/JSON results + downloadable resumes

## Architectural Patterns

### Modular Design
- Clear separation of concerns (parsing, extraction, matching)
- Each module has single responsibility
- Easy to extend and maintain

### Configuration-Driven
- Scoring weights externalized to config.json
- Skills taxonomy in separate JSON file
- Environment-based database configuration

### Multiple Interfaces
- Web UI for interactive use
- CLI for batch processing
- API for integration

### Database Integration
- PostgreSQL for persistent storage
- Results tracking and analytics
- User authentication and sessions
