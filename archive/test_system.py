"""
Quick test script to verify all components work
"""

print("Testing Resume Screening System Components...")
print("=" * 60)

# Test 1: Import all modules
print("\n1. Testing imports...")
try:
    from parsers import ResumeParser, JDParser
    from extractors import KeywordExtractor
    from matcher import ResumeScorer
    print("   [OK] All modules imported successfully")
except Exception as e:
    print(f"   [ERROR] Import failed: {e}")
    exit(1)

# Test 2: Initialize components
print("\n2. Testing component initialization...")
try:
    resume_parser = ResumeParser()
    jd_parser = JDParser()
    extractor = KeywordExtractor('data/skills_taxonomy.json')
    scorer = ResumeScorer('data/config.json')
    print("   [OK] All components initialized")
except Exception as e:
    print(f"   [ERROR] Initialization failed: {e}")
    exit(1)

# Test 3: Parse job description
print("\n3. Testing job description parsing...")
try:
    jd_data = jd_parser.parse_file('input/job_description.txt')
    print(f"   [OK] JD parsed: {len(jd_data['required_skills'])} required skills")
except Exception as e:
    print(f"   [ERROR] JD parsing failed: {e}")
    exit(1)

# Test 4: Parse a sample resume
print("\n4. Testing resume parsing...")
try:
    resume = resume_parser.parse_file('input/REAL_0001_Chad_Griffin.pdf')
    print(f"   [OK] Resume parsed: {len(resume['text'])} characters")
except Exception as e:
    print(f"   [ERROR] Resume parsing failed: {e}")
    exit(1)

# Test 5: Extract skills
print("\n5. Testing skill extraction...")
try:
    skills = extractor.extract_skills(resume['text'])
    experience = extractor.extract_experience_years(resume['text'])
    keywords = extractor.extract_keywords(resume['text'])
    print(f"   [OK] Extracted {len(skills)} skills, {experience} years exp")
except Exception as e:
    print(f"   [ERROR] Extraction failed: {e}")
    exit(1)

# Test 6: Score resume
print("\n6. Testing scoring...")
try:
    score = scorer.score_resume(skills, experience, keywords, jd_data)
    print(f"   [OK] Score calculated: {score['total_score']:.1f}%")
except Exception as e:
    print(f"   [ERROR] Scoring failed: {e}")
    exit(1)

print("\n" + "=" * 60)
print("ALL TESTS PASSED!")
print("=" * 60)
print("\nYour Resume Screening System is working correctly!")
print("\nNext steps:")
print("  1. Run CLI: python main.py --jd input/job_description.txt --resumes input/ --top 10")
print("  2. Run Web UI: streamlit run app.py")
