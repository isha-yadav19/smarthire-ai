# Technology Stack

## Programming Languages
- **Python 3.8+**: Core language for all modules

## Core Dependencies

### Document Processing
- **PyPDF2 >= 3.0.1**: PDF text extraction and parsing
- **python-docx >= 1.2.0**: DOCX file parsing
- **reportlab >= 4.0.0**: PDF generation for JSONL conversion

### Web Framework
- **Streamlit >= 1.28.0**: Primary web interface framework
  - Interactive UI components
  - File upload handling
  - Real-time processing display
  - Built-in session state management

### API Framework
- **Flask >= 3.0.0**: REST API server
- **Flask-CORS >= 4.0.0**: Cross-origin resource sharing

### Data Processing
- **Pandas >= 2.0.0**: Data manipulation and CSV/JSON export
  - DataFrame operations
  - Result aggregation
  - Export functionality

### Database
- **PostgreSQL**: Primary database (external)
- **psycopg2-binary >= 2.9.9**: PostgreSQL adapter for Python
- **python-dotenv >= 1.0.0**: Environment variable management

### Authentication & Security
- **bcrypt >= 4.1.1**: Password hashing and verification
- Secure session management
- User authentication system

## Development Tools

### Package Management
- **pip**: Python package installer
- **requirements.txt**: Dependency specification

### Version Control
- **Git**: Source control
- **.gitignore**: Configured for Python projects

## Build & Run Commands

### Environment Setup
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\Activate.ps1

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

#### Web Interface (Primary)
```bash
streamlit run app.py
# Access at http://localhost:8501
```

#### CLI Processing
```bash
python main.py
# Processes files from input/ folder
```

#### API Server
```bash
python api_server.py
# REST API endpoints available
```

#### Dashboard
```bash
streamlit run dashboard.py
# Analytics interface
```

### Network Deployment
```bash
# Local network access
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
# Access from other devices: http://<your-ip>:8501
```

### Testing
```bash
# Test PDF parsing
python test_pdf_parsing.py

# Test resume conversion
python convert_to_pdf.py
```

## Configuration Files

### Streamlit Configuration (`.streamlit/config.toml`)
- Server settings
- Upload limits (default 500MB)
- Theme customization
- Port configuration

### Environment Variables (`.env`)
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=resume_db
DB_USER=<username>
DB_PASSWORD=<password>
```

### Application Config (`data/config.json`)
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

## Performance Characteristics
- **Processing speed**: ~2-5 resumes/second
- **Batch capacity**: Up to 1000 resumes (memory dependent)
- **Upload limit**: 500MB (configurable)
- **Accuracy**: 85-90% skill matching

## Deployment Options

### Streamlit Cloud (Free)
1. Push to GitHub
2. Connect at share.streamlit.io
3. Select app.py as main file
4. Auto-deploys on push

### Local Server
- Run on local network
- Configure firewall rules
- Set server address to 0.0.0.0

### Docker (Future)
- Containerization support planned
- Multi-service orchestration

## Database Schema
- Defined in `schema.sql`
- PostgreSQL-specific features
- Tables for users, results, analytics

## Python Version Requirements
- **Minimum**: Python 3.8
- **Recommended**: Python 3.10+
- Compatible with Windows, Linux, macOS

## External Services
- **PostgreSQL Database**: Required for persistence
- **Streamlit Cloud**: Optional for deployment
- **GitHub**: Version control and deployment source
