"""
SmartHire.AI - Flask API Backend
Handles authentication requests from login page
"""

from flask import Flask, request, jsonify, session, redirect, url_for, send_from_directory
from flask_cors import CORS
try:
    from auth_manager_simple import AuthManager
    print("[OK] Using simple file-based authentication (no PostgreSQL required)")
except ImportError:
    from auth_manager import AuthManager
    print("[OK] Using PostgreSQL authentication")
import os
import sys
import json
import tempfile
import shutil
from pathlib import Path
from datetime import timedelta
from werkzeug.utils import secure_filename

# Ensure backend/ submodules are importable
BASE_DIR = Path(__file__).parent          # backend/
ROOT_DIR = BASE_DIR.parent                # project root
sys.path.insert(0, str(BASE_DIR))

# Resume processing imports
from parsers import ResumeParser, JDParser
from extractors import KeywordExtractor
from matcher import ResumeScorer

app = Flask(__name__, static_folder=str(ROOT_DIR), static_url_path='')
app.secret_key = os.environ.get('SECRET_KEY', 'smarthire-dev-secret-key-2026')
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('FLASK_ENV') == 'production'
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=8)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB
CORS(app, supports_credentials=True)

auth_manager = AuthManager()

# Ensure demo users always exist (survives fresh deploys)
def _seed_demo_users():
    demo = [
        ('ada', 'ada@smarthire.ai', 'demo123', 'recruiter'),
        ('isha', 'isha@smarthire.ai', 'demo123', 'candidate'),
    ]
    for username, email, password, role in demo:
        if username not in auth_manager.users:
            auth_manager.register_user(username, email, password, role)
            print(f"[SEED] Created demo user: {username}")
        else:
            # Reset password to demo123 in case it changed
            auth_manager.users[username]['password_hash'] = auth_manager.hash_password(password)
            auth_manager._save_users(auth_manager.users)

_seed_demo_users()

# Upload folder — always relative to project root
UPLOAD_FOLDER = ROOT_DIR / 'uploads'
UPLOAD_FOLDER.mkdir(exist_ok=True)

# Load processing components once — paths relative to project root
config_path = ROOT_DIR / 'data' / 'config.json'
taxonomy_path = ROOT_DIR / 'data' / 'skills_taxonomy.json'
resume_parser = ResumeParser()
jd_parser = JDParser()
extractor = KeywordExtractor(str(taxonomy_path))
scorer = ResumeScorer(str(config_path) if config_path.exists() else None)

@app.route('/api/login', methods=['POST'])
def login():
    """Handle login request"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')
        
        if not username or not password:
            return jsonify({
                "success": False,
                "message": "Username and password required"
            }), 400
        
        # Authenticate user
        result = auth_manager.login(username, password)
        
        if result['success']:
            # Check if role matches
            if result['user']['role'] != role:
                return jsonify({
                    "success": False,
                    "message": f"Invalid role. This account is registered as {result['user']['role']}"
                }), 403
            
            # Create session
            session.permanent = True
            session['user_id'] = result['user']['id']
            session['username'] = result['user']['username']
            session['role'] = result['user']['role']
            
            return jsonify({
                "success": True,
                "message": "Login successful",
                "user": result['user'],
                "redirect": "/dashboard"
            }), 200
        else:
            return jsonify(result), 401
    
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Server error: {str(e)}"
        }), 500

@app.route('/api/logout', methods=['POST'])
def logout():
    """Handle logout"""
    session.clear()
    return jsonify({
        "success": True,
        "message": "Logged out successfully"
    }), 200

@app.route('/api/check-session', methods=['GET'])
def check_session():
    """Check if user is logged in"""
    if 'user_id' in session:
        return jsonify({
            "logged_in": True,
            "user": {
                "id": session['user_id'],
                "username": session['username'],
                "role": session['role']
            }
        }), 200
    else:
        return jsonify({
            "logged_in": False
        }), 200

@app.route('/api/register', methods=['POST'])
def register():
    """Handle user registration (public)"""
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'recruiter')
        
        if not all([username, email, password]):
            return jsonify({
                "success": False,
                "message": "All fields required"
            }), 400
        
        result = auth_manager.register_user(username, email, password, role)
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
    
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Registration error: {str(e)}"
        }), 500

@app.route('/api/reset-password', methods=['POST'])
def reset_password():
    """Handle password reset"""
    try:
        data = request.get_json()
        email = data.get('email')
        
        if not email:
            return jsonify({
                "success": False,
                "message": "Email required"
            }), 400
        
        # Generate new random password
        import secrets
        import string
        new_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(10))
        
        # Find user and update password
        user_found = False
        for user in auth_manager.users.values():
            if user['email'] == email:
                user_found = True
                user['password_hash'] = auth_manager.hash_password(new_password)
                auth_manager._save_users(auth_manager.users)
                break
        
        if user_found:
            return jsonify({
                "success": True,
                "message": "Password reset successful",
                "new_password": new_password
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "No account found with that email"
            }), 404
    
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Password reset error: {str(e)}"
        }), 500

@app.route('/api/upload', methods=['POST'])
def upload():
    """Handle resume file uploads"""
    try:
        files = request.files.getlist('files')
        if not files:
            return jsonify({"success": False, "message": "No files provided"}), 400

        uploaded = []
        for file in files:
            if file and file.filename:
                filename = secure_filename(file.filename)
                filepath = UPLOAD_FOLDER / filename
                file.save(str(filepath))
                uploaded.append(filename)

        return jsonify({"success": True, "uploaded": uploaded, "count": len(uploaded)}), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/api/process', methods=['POST'])
def process():
    """Process uploaded resumes against a job description"""
    try:
        data = request.get_json()
        job_description = data.get('job_description', '')
        top_n = int(data.get('top_n', 10))
        min_score = data.get('min_score') or 0

        if not job_description:
            return jsonify({"success": False, "message": "Job description required"}), 400

        # Parse JD from text
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as tmp:
            tmp.write(job_description)
            tmp_path = tmp.name

        try:
            jd_data = jd_parser.parse_file(tmp_path)
        finally:
            Path(tmp_path).unlink(missing_ok=True)

        # Load uploaded resumes
        resume_files = list(UPLOAD_FOLDER.glob('*.pdf')) + list(UPLOAD_FOLDER.glob('*.docx'))
        if not resume_files:
            return jsonify({"success": False, "message": "No resumes found. Please upload first."}), 400

        # Score each resume
        scored = []
        for rf in resume_files:
            try:
                resume = resume_parser.parse_file(str(rf))
                skills = extractor.extract_skills(resume['text'])
                experience = extractor.extract_experience_years(resume['text'])
                keywords = extractor.extract_keywords(resume['text'])
                score = scorer.score_resume(skills, experience, keywords, jd_data)
                scored.append({
                    'name': resume.get('name', rf.stem),
                    'email': resume.get('email', ''),
                    'phone': resume.get('phone', ''),
                    'filename': rf.name,
                    'total_score': round(score['total_score'], 1),
                    'experience_years': experience,
                    'matched_skills': score['matched_required_skills'],
                    'missing_skills': score['missing_required_skills'],
                    'scores': {
                        'required_skills': round(score['required_skills_score'], 1),
                        'preferred_skills': round(score['preferred_skills_score'], 1),
                        'experience': round(score['experience_score'], 1),
                        'keyword': round(score['keyword_score'], 1),
                    }
                })
            except Exception as e:
                print(f"[WARN] Skipped {rf.name}: {e}")
                continue

        # Filter and sort
        if min_score:
            scored = [r for r in scored if r['total_score'] >= float(min_score)]
        scored.sort(key=lambda x: x['total_score'], reverse=True)
        results = scored[:top_n]

        return jsonify({
            "success": True,
            "results": results,
            "total_processed": len(scored),
            "top_n": len(results)
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


APPLICATIONS_FILE = ROOT_DIR / 'data' / 'applications.json'

def _load_applications():
    if APPLICATIONS_FILE.exists():
        with open(APPLICATIONS_FILE, 'r') as f:
            return json.load(f).get('applications', [])
    return []

def _save_applications(apps):
    with open(APPLICATIONS_FILE, 'w') as f:
        json.dump({'applications': apps}, f, indent=2)

@app.route('/api/apply', methods=['POST'])
def apply():
    """Save a candidate application"""
    try:
        data = request.get_json()
        apps = _load_applications()
        app_record = {
            'id': int(__import__('time').time() * 1000),
            'job_id': data.get('job_id'),
            'job_title': data.get('job_title', ''),
            'company': data.get('company', ''),
            'candidate_name': data.get('candidate_name', ''),
            'candidate_email': data.get('candidate_email', ''),
            'match_percentage': data.get('match_percentage', 0),
            'missing_skills': data.get('missing_skills', []),
            'applied_date': data.get('applied_date', ''),
            'status': 'Applied'
        }
        apps.append(app_record)
        _save_applications(apps)
        return jsonify({'success': True, 'application': app_record}), 201
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/applications', methods=['GET'])
def get_applications():
    """Get all applications — optionally filter by job_id or candidate_email"""
    try:
        apps = _load_applications()
        job_id = request.args.get('job_id')
        email = request.args.get('email')
        if job_id:
            apps = [a for a in apps if str(a.get('job_id')) == str(job_id)]
        if email:
            apps = [a for a in apps if a.get('candidate_email') == email]
        return jsonify({'success': True, 'applications': apps}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/applications/<int:app_id>/status', methods=['PATCH'])
def update_application_status(app_id):
    """Update application status (Shortlisted/Rejected)"""
    try:
        data = request.get_json()
        status = data.get('status')
        apps = _load_applications()
        for a in apps:
            if a['id'] == app_id:
                a['status'] = status
                _save_applications(apps)
                return jsonify({'success': True}), 200
        return jsonify({'success': False, 'message': 'Application not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/clear-uploads', methods=['POST'])
def clear_uploads():
    """Clear uploaded files"""
    shutil.rmtree(str(UPLOAD_FOLDER), ignore_errors=True)
    UPLOAD_FOLDER.mkdir(exist_ok=True)
    return jsonify({"success": True}), 200


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "SmartHire.AI API"
    }), 200

# --- Static file serving (for deployment) ---
@app.route('/')
def index():
    return send_from_directory(str(ROOT_DIR / 'auth'), 'landing.html')

@app.route('/auth/<path:filename>')
def auth_files(filename):
    return send_from_directory(str(ROOT_DIR / 'auth'), filename)

@app.route('/candidate')
def candidate():
    return send_from_directory(str(ROOT_DIR), 'candidate_dashboard.html')

@app.route('/recruiter')
def recruiter():
    return send_from_directory(str(ROOT_DIR), 'recruiter_dashboard.html')

@app.route('/data/<path:filename>')
def data_files(filename):
    return send_from_directory(str(ROOT_DIR / 'data'), filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    print(f"SmartHire.AI running on http://localhost:{port}")
    app.run(debug=debug, host='0.0.0.0', port=port)
