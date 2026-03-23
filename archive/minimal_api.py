from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/api/upload', methods=['POST'])
def upload():
    print("\n" + "="*50)
    print("UPLOAD REQUEST RECEIVED")
    print("="*50)
    
    files = request.files.getlist('files')
    print(f"Number of files: {len(files)}")
    
    uploaded = []
    for file in files:
        if file and file.filename:
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            uploaded.append(filename)
            print(f"✓ Saved: {filename}")
    
    print(f"Total uploaded: {len(uploaded)}")
    print("="*50 + "\n")
    
    return jsonify({
        "success": True,
        "uploaded": uploaded,
        "count": len(uploaded)
    })

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({"status": "API is working!"})

if __name__ == '__main__':
    print("\n" + "="*50)
    print("MINIMAL API SERVER RUNNING")
    print("http://localhost:5000")
    print("="*50 + "\n")
    app.run(host='0.0.0.0', port=5000, debug=True)
