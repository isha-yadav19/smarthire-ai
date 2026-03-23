"""
SmartHire.AI - Resume Processing API
Connects beautiful HTML dashboards to real AI processing engine
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import tempfile
import shutil
from pathlib import Path
import json
from datetime import datetime

from parsers import ResumeParser, JDParser
from extractors import KeywordExtractor
from matcher import ResumeScorer

app = Flask(__name__)
CORS(app)

# Initialize components
config_path = Path(__file__).parent / 'data' / 'config.json'
taxonomy_path = Path(__file__).parent / 'data' / 'skills_taxonomy.json'

resume_parser = ResumeParser()
jd_parser = JDParser()
extractor = KeywordExtractor(str(taxonomy_path))
scorer = ResumeScorer(str(config_path) if config_path.exists() else None)

@app.route('/api/process-resumes', methods=['POST'])
def process_resumes():
    """Process uploaded resumes against job description"""
    try:
        # Get job description
        jd_text = request.form.get('job_description')
        if not jd_text:
            return jsonify({'success': False, 'message': 'Job description required'}), 400
        
        # Get uploaded files
        files = request.files.getlist('resumes')
        if not files:
            return jsonify({'success': False, 'message': 'No resumes uploaded'}), 400
        
        # Parse job description
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as tmp:
            tmp.write(jd_text)
            tmp_path = tmp.name
        
        jd_data = jd_parser.parse_file(tmp_path)
        Path(tmp_path).unlink()
        
        # Create temp directory for resumes
        temp_dir = tempfile.mkdtemp()
        results = []
        
        try:
            # Process each resume
            for file in files:
                # Save file
                file_path = Path(temp_dir) / file.filename
                file.save(str(file_path))
                
                # Parse resume
                resume = resume_parser.parse_file(str(file_path))
                
                # Extract features
                resume_skills = extractor.extract_skills(resume['text'])
                resume_experience = extractor.extract_experience_years(resume['text'])
                resume_keywords = extractor.extract_keywords(resume['text'])
                
                # Score resume
                score = scorer.score_resume(
                    resume_skills, resume_experience, resume_keywords, jd_data
                )
                
                results.append({
                    'filename': file.filename,
                    'name': resume.get('name', 'Unknown'),
                    'email': resume.get('email', ''),
                    'phone': resume.get('phone', ''),
                    'total_score': round(score['total_score'], 1),
                    'required_skills_score': round(score['required_skills_score'], 1),
                    'preferred_skills_score': round(score['preferred_skills_score'], 1),
                    'experience_score': round(score['experience_score'], 1),
                    'keyword_score': round(score['keyword_score'], 1),
                    'matched_skills': score['matched_required_skills'],
                    'missing_skills': score['missing_required_skills'],
                    'experience_years': resume_experience
                })
        
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
        
        # Sort by score
        results.sort(key=lambda x: x['total_score'], reverse=True)
        
        return jsonify({
            'success': True,
            'results': results,
            'total_processed': len(results)
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/analyze-ats', methods=['POST'])
def analyze_ats():
    """Analyze ATS compatibility of resume"""
    try:
        jd_text = request.form.get('job_description')
        file = request.files.get('resume')
        
        if not jd_text or not file:
            return jsonify({'success': False, 'message': 'Resume and JD required'}), 400
        
        # Parse JD
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as tmp:
            tmp.write(jd_text)
            tmp_path = tmp.name
        
        jd_data = jd_parser.parse_file(tmp_path)
        Path(tmp_path).unlink()
        
        # Parse resume
        temp_dir = tempfile.mkdtemp()
        file_path = Path(temp_dir) / file.filename
        file.save(str(file_path))
        
        resume = resume_parser.parse_file(str(file_path))
        resume_skills = extractor.extract_skills(resume['text'])
        resume_experience = extractor.extract_experience_years(resume['text'])
        resume_keywords = extractor.extract_keywords(resume['text'])
        
        score = scorer.score_resume(
            resume_skills, resume_experience, resume_keywords, jd_data
        )
        
        shutil.rmtree(temp_dir, ignore_errors=True)
        
        return jsonify({
            'success': True,
            'ats_score': round(score['total_score'], 1),
            'keywords_matched': len(score['matched_required_skills']),
            'skills_alignment': round(score['required_skills_score'], 1),
            'format_score': 95,  # Placeholder
            'recommendations': [
                f"Keywords matched: {len(score['matched_required_skills'])}",
                f"Skills alignment: {round(score['required_skills_score'], 1)}%",
                "Format: ATS-friendly",
                f"Experience: {resume_experience} years"
            ]
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'SmartHire.AI Processing API'})

if __name__ == '__main__':
    print("=" * 60)
    print("SmartHire.AI Processing API")
    print("=" * 60)
    print("Server running on: http://localhost:5001")
    print("Endpoints:")
    print("  POST /api/process-resumes - Process resumes against JD")
    print("  POST /api/analyze-ats      - Analyze ATS compatibility")
    print("  GET  /health               - Health check")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5001)
