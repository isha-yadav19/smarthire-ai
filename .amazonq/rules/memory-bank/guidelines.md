# Development Guidelines

## Code Quality Standards

### Documentation
- **Module docstrings**: Every module starts with triple-quoted docstring explaining purpose
  ```python
  """
  Convert JSONL resumes to PDF format
  Extracts 500 resumes and creates individual PDF files
  """
  ```
- **Function docstrings**: Brief descriptions for all functions
  ```python
  def create_resume_pdf(resume_data: dict, output_path: str):
      """Create a PDF file from resume data"""
  ```
- **Inline comments**: Explain complex logic and business rules
  ```python
  # Extract username from email (before @)
  username = email.split('@')[0]
  ```

### Naming Conventions
- **Variables**: snake_case for all variables
  - `resume_data`, `output_path`, `text_length`, `selected_role`
- **Functions**: snake_case with descriptive verbs
  - `create_resume_pdf()`, `convert_jsonl_to_pdfs()`, `test_pdf_parsing()`
- **Constants**: UPPERCASE for API endpoints and configuration
  - `API_URL = 'http://localhost:5000/api'`
- **Classes**: PascalCase (implied from imports)
  - `ResumeParser`, `KeywordExtractor`
- **Files**: snake_case for Python modules
  - `resume_parser.py`, `keyword_extractor.py`, `test_pdf_parsing.py`

### Code Formatting
- **Indentation**: 4 spaces (Python standard)
- **Line length**: Reasonable limits, break long lines logically
- **Blank lines**: 
  - 2 blank lines between top-level functions
  - 1 blank line between logical sections within functions
- **String quotes**: Single quotes for JavaScript, double quotes for Python strings
- **f-strings**: Preferred for string formatting in Python
  ```python
  print(f"Converting {limit} resumes to PDF...")
  print(f"Output directory: {output_path.absolute()}")
  ```

## Structural Conventions

### Error Handling
- **Try-except blocks**: Wrap risky operations with specific error handling
  ```python
  try:
      resume = json.loads(line)
      # ... processing
  except Exception as e:
      errors += 1
      print(f"  Error on line {line_num}: {e}")
      continue
  ```
- **Graceful degradation**: Continue processing on individual failures
- **User-friendly messages**: Clear error descriptions with actionable guidance
  ```javascript
  alert('Connection error. Make sure the backend server is running.\n\nRun: python api_server.py');
  ```

### Import Organization
- **Standard library first**: Built-in modules at top
  ```python
  import json
  import os
  from pathlib import Path
  ```
- **Third-party next**: External dependencies after standard library
  ```python
  from reportlab.lib.pagesizes import letter
  from reportlab.lib.styles import getSampleStyleSheet
  ```
- **Local imports last**: Project modules at end
  ```python
  from parsers.resume_parser import ResumeParser
  from .keyword_extractor import KeywordExtractor
  ```
- **Lazy imports with fallback**: Install missing dependencies automatically
  ```python
  try:
      from reportlab.lib.pagesizes import letter
  except ImportError:
      print("Installing reportlab...")
      os.system("pip install reportlab")
      from reportlab.lib.pagesizes import letter
  ```

### Package Structure
- **__init__.py files**: Export public API explicitly
  ```python
  from .keyword_extractor import KeywordExtractor
  __all__ = ['KeywordExtractor']
  ```
- **Relative imports**: Use relative imports within packages
  ```python
  from .keyword_extractor import KeywordExtractor
  ```

## Practices Followed

### Path Handling
- **pathlib.Path**: Use Path objects for cross-platform compatibility
  ```python
  output_path = Path(output_dir)
  output_path.mkdir(parents=True, exist_ok=True)
  pdf_files = list(input_dir.glob('REAL_*.pdf'))
  ```
- **Absolute paths**: Convert to absolute for clarity
  ```python
  print(f"📁 PDFs saved to: {output_path.absolute()}")
  ```

### User Feedback
- **Progress indicators**: Show progress for long operations
  ```python
  if converted % 50 == 0:
      print(f"  Converted {converted}/{limit} resumes...")
  ```
- **Visual separators**: Use symbols and lines for readability
  ```python
  print("=" * 60)
  print(f"✓ Successfully converted {converted} resumes to PDF")
  ```
- **Emoji indicators**: Use emojis for status (✓, ✗, 📁, 📦, 🐍, 🔍)
  ```python
  print(f"✓ {module} ({description})")
  print(f"❌ {module} - NOT INSTALLED")
  ```

### Configuration Management
- **Environment variables**: Use .env for sensitive data
- **JSON config files**: External configuration for weights and parameters
- **Default values**: Provide sensible defaults with override capability
  ```python
  def convert_jsonl_to_pdfs(jsonl_path: str, output_dir: str, limit: int = 500):
  ```

### Testing Patterns
- **Validation scripts**: Separate test files for verification
  - `test_pdf_parsing.py` validates PDF parsing reliability
- **Success metrics**: Calculate and report success rates
  ```python
  print(f"Success: {success}/{len(pdf_files)} ({success/len(pdf_files)*100:.1f}%)")
  ```
- **Verdict system**: Provide actionable recommendations
  ```python
  if success >= 8:
      print("[VERDICT] PDF parsing is RELIABLE - KEEP IT")
  ```

## Semantic Patterns

### Async/Await (JavaScript)
- **Async form handling**: Use async/await for API calls
  ```javascript
  loginForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const response = await fetch(`${API_URL}/login`, {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({username, password, role})
      });
  });
  ```

### Data Processing Pipeline
- **Batch processing**: Process items in chunks with progress tracking
- **Counter tracking**: Maintain success/failure counters
  ```python
  converted = 0
  errors = 0
  # ... processing loop
  converted += 1
  ```
- **Early exit**: Check limits and break when reached
  ```python
  if converted >= limit:
      break
  ```

### File Operations
- **Safe filename generation**: Sanitize filenames for cross-platform compatibility
  ```python
  filename = f"{resume_id}_{name}.pdf"
  filename = "".join(c for c in filename if c.isalnum() or c in ('_', '-', '.'))
  ```
- **Directory creation**: Create directories with parents and exist_ok
  ```python
  output_path.mkdir(parents=True, exist_ok=True)
  ```

### String Sanitization
- **HTML escaping**: Escape special characters for safe rendering
  ```python
  clean_summary = summary[:500].replace('<', '&lt;').replace('>', '&gt;')
  ```
- **Truncation**: Limit text length to prevent overflow
  ```python
  clean_exp = experience[:1500].replace('<', '&lt;').replace('>', '&gt;')
  ```

## Internal API Usage

### ResumeParser API
```python
from parsers.resume_parser import ResumeParser

parser = ResumeParser()
result = parser.parse_file(str(pdf_file))
text_length = len(result['text'])
```

### KeywordExtractor API
```python
from extractors import KeywordExtractor

extractor = KeywordExtractor()
# Usage implied from package structure
```

### ReportLab PDF Generation
```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

doc = SimpleDocTemplate(output_path, pagesize=letter,
                        rightMargin=72, leftMargin=72,
                        topMargin=72, bottomMargin=72)
styles = getSampleStyleSheet()
story = []
story.append(Paragraph(text, styles['Heading1']))
story.append(Spacer(1, 0.2 * inch))
doc.build(story)
```

### Fetch API (JavaScript)
```javascript
const response = await fetch(`${API_URL}/login`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({username, password, role})
});
const data = await response.json();
```

## Common Idioms

### Dictionary Access with Defaults
```python
name = resume_data.get('Name', 'Unknown')
email = resume_data.get('Email', '')
phone = resume_data.get('Phone', '')[:20] if resume_data.get('Phone') else ''
```

### Conditional String Truncation
```python
phone = resume_data.get('Phone', '')[:20] if resume_data.get('Phone') else ''
```

### List Comprehension for Filtering
```python
filename = "".join(c for c in filename if c.isalnum() or c in ('_', '-', '.'))
```

### Enumerate with Start Index
```python
for line_num, line in enumerate(f, 1):
    # line_num starts at 1 instead of 0
```

### Session Storage (JavaScript)
```javascript
sessionStorage.setItem('user', JSON.stringify(data.user));
window.location.href = 'http://localhost:8501';
```

### DOM Manipulation (JavaScript)
```javascript
const roleTabs = document.querySelectorAll('.role-tab');
roleTabs.forEach(tab => {
    tab.addEventListener('click', () => {
        roleTabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
    });
});
```

## Annotations & Type Hints

### Function Type Hints
```python
def create_resume_pdf(resume_data: dict, output_path: str):
def convert_jsonl_to_pdfs(jsonl_path: str, output_dir: str, limit: int = 500):
```

### Return Type Hints (Implied)
- Functions return boolean for success/failure
- Functions return dictionaries for structured data
- Functions return None for side-effect operations

## Setup & Installation Patterns

### Subprocess Execution
```python
result = subprocess.run(command, shell=True, check=True, 
                       capture_output=True, text=True)
```

### Module Verification
```python
try:
    __import__(module)
    print(f"   ✓ {module} ({description})")
except ImportError:
    print(f"   ❌ {module} - NOT INSTALLED")
```

### Version Checking
```python
version = sys.version_info
if version.major < 3 or (version.major == 3 and version.minor < 8):
    print("❌ Python 3.8 or higher is required!")
    return False
```

## Best Practices Summary

1. **Always provide user feedback** for long-running operations
2. **Handle errors gracefully** and continue processing when possible
3. **Use pathlib.Path** for all file system operations
4. **Sanitize user input** and file names for security
5. **Document all modules and functions** with docstrings
6. **Use type hints** for function parameters
7. **Provide default values** for optional parameters
8. **Track metrics** (success/failure counts) for operations
9. **Use f-strings** for string formatting
10. **Separate concerns** into distinct modules (parsers, extractors, matchers)
