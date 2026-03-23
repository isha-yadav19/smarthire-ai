from flask import Flask, request, jsonify, session
from flask_cors import CORS
from auth_manager_simple import AuthManager
import os
from datetime import timedelta
from pathlib import Path
from werkzeug.utils import secure_filename
import tempfile
import shutil
from parsers import ResumeParser, JDParser
from extractors import KeywordExtractor
from matcher import ResumeScorer

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_COOKIE_SECURE'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=8)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max upload
app.config['UPLOAD_FOLDER'] = 'uploads'
CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}})

auth_manager = AuthManager()

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

# Create upload directory
Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)

# Initialize screening components
config_path = Path(__file__).parent / 'data' / 'config.json'
taxonomy_path = Path(__file__).parent / 'data' / 'skills_taxonomy.json'
resume_parser = ResumeParser()
jd_parser = JDParser()
extractor = KeywordExtractor(str(taxonomy_path))
scorer = ResumeScorer(str(config_path) if config_path.exists() else None)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')
        
        if not username or not password:
            return jsonify({"success": False, "message": "Username and password required"}), 400
        
        result = auth_manager.login(username, password)
        
        if result['success']:
            if result['user']['role'] != role:
                return jsonify({"success": False, "message": f"Invalid role. This account is registered as {result['user']['role']}"}), 403
            
            session.permanent = True
            session['user_id'] = result['user']['id']
            session['username'] = result['user']['username']
            session['role'] = result['user']['role']
            
            return jsonify({"success": True, "message": "Login successful", "user": result['user'], "redirect": "/dashboard"}), 200
        else:
            return jsonify(result), 401
    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500

@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'recruiter')
        
        if not all([username, email, password]):
            return jsonify({"success": False, "message": "All fields required"}), 400
        
        result = auth_manager.register_user(username, email, password, role)
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
    except Exception as e:
        return jsonify({"success": False, "message": f"Registration error: {str(e)}"}), 500

@app.route('/api/upload', methods=['POST', 'OPTIONS'])
def upload_resumes():
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        print("\n=== Upload Request ===")
        print(f"Content-Type: {request.content_type}")
        print(f"Files keys: {list(request.files.keys())}")
        print(f"Form keys: {list(request.form.keys())}")
        
        files = request.files.getlist('files')
        if not files:
            files = request.files.getlist('file')
        
        print(f"Files received: {len(files)}")
        
        if not files or len(files) == 0:
            return jsonify({"success": False, "message": "No files provided"}), 400
        
        uploaded_files = []
        errors = []
        
        for file in files:
            if file and file.filename:
                print(f"Processing file: {file.filename}")
                if allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    uploaded_files.append(filename)
                    print(f"  ✓ Saved: {filename}")
                else:
                    error_msg = f"{file.filename}: Invalid file type (only PDF and DOCX allowed)"
                    errors.append(error_msg)
                    print(f"  ✗ {error_msg}")
        
        if len(uploaded_files) == 0:
            return jsonify({
                "success": False,
                "message": "No valid files uploaded",
                "errors": errors
            }), 400
        
        print(f"\n✓ Successfully uploaded {len(uploaded_files)} files")
        return jsonify({
            "success": True,
            "message": f"Uploaded {len(uploaded_files)} file(s)",
            "uploaded": uploaded_files,
            "errors": errors
        }), 200
        
    except Exception as e:
        print(f"\n✗ Upload error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "message": f"Upload error: {str(e)}"}), 500

@app.route('/api/process', methods=['POST'])
def process_resumes():
    try:
        data = request.get_json()
        job_description = data.get('job_description')
        top_n = data.get('top_n', 10)
        min_score = data.get('min_score')
        
        if not job_description:
            return jsonify({"success": False, "message": "Job description required"}), 400
        
        # Get uploaded files
        upload_dir = Path(app.config['UPLOAD_FOLDER'])
        resume_files = list(upload_dir.glob('*.pdf')) + list(upload_dir.glob('*.docx'))
        
        if not resume_files:
            return jsonify({"success": False, "message": "No resume files found. Upload files first."}), 400
        
        # Parse JD
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as tmp:
            tmp.write(job_description)
            tmp_path = tmp.name
        
        try:
            jd_data = jd_parser.parse_file(tmp_path)
        finally:
            Path(tmp_path).unlink()
        
        # Parse and score resumes
        resumes = []
        for file_path in resume_files:
            try:
                resume = resume_parser.parse_file(str(file_path))
                resume['filename'] = file_path.name
                resumes.append(resume)
            except Exception as e:
                print(f"Error parsing {file_path.name}: {e}")
        
        if not resumes:
            return jsonify({"success": False, "message": "No resumes could be parsed"}), 400
        
        # Score resumes
        scored_resumes = []
        for resume in resumes:
            resume_skills = extractor.extract_skills(resume['text'])
            resume_experience = extractor.extract_experience_years(resume['text'])
            resume_keywords = extractor.extract_keywords(resume['text'])
            
            score = scorer.score_resume(resume_skills, resume_experience, resume_keywords, jd_data)
            
            scored_resumes.append({
                'filename': resume.get('filename', 'Unknown'),
                'name': resume.get('name', 'Unknown'),
                'email': resume.get('email', ''),
                'phone': resume.get('phone', ''),
                'total_score': score['total_score'],
                'required_skills_score': score['required_skills_score'],
                'preferred_skills_score': score['preferred_skills_score'],
                'experience_score': score['experience_score'],
                'keyword_score': score['keyword_score'],
                'experience_years': score['resume_experience'],
                'matched_skills': score['matched_required_skills'][:10],
                'missing_skills': score['missing_required_skills'][:10]
            })
        
        # Filter and rank
        if min_score:
            scored_resumes = [r for r in scored_resumes if r['total_score'] >= min_score]
        
        ranked_resumes = sorted(scored_resumes, key=lambda x: x['total_score'], reverse=True)
        top_resumes = ranked_resumes[:top_n]
        
        # Clean up uploaded files
        for file_path in resume_files:
            try:
                file_path.unlink()
            except:
                pass
        
        return jsonify({
            "success": True,
            "message": f"Processed {len(resumes)} resumes",
            "total_processed": len(resumes),
            "results": top_resumes
        }), 200
        
    except Exception as e:
        print(f"Processing error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "message": f"Processing error: {str(e)}"}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "SmartHire.AI API"}), 200

if __name__ == '__main__':
    print("=" * 60)
    print("SmartHire.AI Backend Server")
    print("=" * 60)
    print("Server running on: http://localhost:5000")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
