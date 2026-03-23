from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from pathlib import Path

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'uploads'
CORS(app)

Path('uploads').mkdir(exist_ok=True)

ALLOWED = {'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED

@app.route('/api/upload', methods=['POST', 'OPTIONS'])
def upload():
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        files = request.files.getlist('files')
        if not files:
            files = request.files.getlist('file')
        
        uploaded = []
        for file in files:
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join('uploads', filename))
                uploaded.append(filename)
        
        return jsonify({
            "success": True,
            "uploaded": uploaded,
            "count": len(uploaded)
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    print("API running on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
