"""
System Test - Verify all components are working
Run this before your exam to ensure everything is ready
"""

import sys
from pathlib import Path

def test_imports():
    """Test all required imports"""
    print("Testing imports...")
    errors = []
    
    modules = [
        ('flask', 'Flask web framework'),
        ('flask_cors', 'CORS support'),
        ('streamlit', 'Streamlit UI'),
        ('pandas', 'Data processing'),
        ('PyPDF2', 'PDF parsing'),
        ('docx', 'DOCX parsing'),
        ('bcrypt', 'Password hashing')
    ]
    
    for module, desc in modules:
        try:
            __import__(module)
            print(f"  ✓ {module} - {desc}")
        except ImportError:
            print(f"  ✗ {module} - NOT INSTALLED")
            errors.append(module)
    
    return len(errors) == 0

def test_project_structure():
    """Test project files and folders exist"""
    print("\nTesting project structure...")
    errors = []
    
    required_files = [
        'simple_api.py',
        'app.py',
        'screen.py',
        'requirements.txt',
        'data/config.json',
        'data/skills_taxonomy.json',
        'parsers/__init__.py',
        'parsers/resume_parser.py',
        'parsers/jd_parser.py',
        'extractors/__init__.py',
        'extractors/keyword_extractor.py',
        'matcher/__init__.py',
        'matcher/scorer.py',
        'auth_manager_simple.py'
    ]
    
    for file in required_files:
        file_path = Path(file)
        if file_path.exists():
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} - MISSING")
            errors.append(file)
    
    return len(errors) == 0

def test_directories():
    """Test required directories"""
    print("\nTesting directories...")
    
    dirs = ['uploads', 'output', 'input', 'data']
    
    for dir_name in dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"  ✓ {dir_name}/")
        else:
            print(f"  ⚠ {dir_name}/ - Creating...")
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"  ✓ {dir_name}/ - Created")
    
    return True

def test_parsers():
    """Test parser modules"""
    print("\nTesting parsers...")
    
    try:
        from parsers import ResumeParser, JDParser
        print("  ✓ ResumeParser imported")
        print("  ✓ JDParser imported")
        
        # Test instantiation
        resume_parser = ResumeParser()
        jd_parser = JDParser()
        print("  ✓ Parsers instantiated successfully")
        
        return True
    except Exception as e:
        print(f"  ✗ Parser error: {e}")
        return False

def test_extractors():
    """Test extractor modules"""
    print("\nTesting extractors...")
    
    try:
        from extractors import KeywordExtractor
        print("  ✓ KeywordExtractor imported")
        
        taxonomy_path = Path('data/skills_taxonomy.json')
        if taxonomy_path.exists():
            extractor = KeywordExtractor(str(taxonomy_path))
            print("  ✓ KeywordExtractor instantiated")
            return True
        else:
            print("  ✗ skills_taxonomy.json not found")
            return False
    except Exception as e:
        print(f"  ✗ Extractor error: {e}")
        return False

def test_matcher():
    """Test matcher module"""
    print("\nTesting matcher...")
    
    try:
        from matcher import ResumeScorer
        print("  ✓ ResumeScorer imported")
        
        config_path = Path('data/config.json')
        if config_path.exists():
            scorer = ResumeScorer(str(config_path))
            print("  ✓ ResumeScorer instantiated")
            return True
        else:
            print("  ⚠ config.json not found - using defaults")
            scorer = ResumeScorer(None)
            print("  ✓ ResumeScorer instantiated with defaults")
            return True
    except Exception as e:
        print(f"  ✗ Matcher error: {e}")
        return False

def test_auth():
    """Test authentication module"""
    print("\nTesting authentication...")
    
    try:
        from auth_manager_simple import AuthManager
        print("  ✓ AuthManager imported")
        
        auth = AuthManager()
        print("  ✓ AuthManager instantiated")
        return True
    except Exception as e:
        print(f"  ✗ Auth error: {e}")
        return False

def test_sample_resumes():
    """Check for sample resumes"""
    print("\nChecking sample resumes...")
    
    input_dir = Path('input')
    if input_dir.exists():
        pdf_files = list(input_dir.glob('*.pdf'))
        docx_files = list(input_dir.glob('*.docx'))
        total = len(pdf_files) + len(docx_files)
        
        print(f"  ✓ Found {len(pdf_files)} PDF files")
        print(f"  ✓ Found {len(docx_files)} DOCX files")
        print(f"  ✓ Total: {total} resume files")
        
        return total > 0
    else:
        print("  ✗ input/ directory not found")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("SmartHire.AI - System Test")
    print("=" * 60)
    print()
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Project Structure", test_project_structure()))
    results.append(("Directories", test_directories()))
    results.append(("Parsers", test_parsers()))
    results.append(("Extractors", test_extractors()))
    results.append(("Matcher", test_matcher()))
    results.append(("Authentication", test_auth()))
    results.append(("Sample Resumes", test_sample_resumes()))
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:8} - {test_name}")
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All tests passed! System is ready for deployment.")
        print("\nNext steps:")
        print("1. Run: START_ALL.bat")
        print("2. Open: http://localhost:8501")
        print("3. Test upload and processing")
        return 0
    else:
        print("\n✗ Some tests failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
