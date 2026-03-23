from flask import Flask, render_template_string, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import json
from pathlib import Path
from datetime import datetime

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'uploads'

os.makedirs('uploads', exist_ok=True)
os.makedirs('output', exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Import your modules
try:
    from parsers import ResumeParser, JDParser
    from extractors import KeywordExtractor
    from matcher import ResumeScorer
    
    config_path = Path('data/config.json')
    taxonomy_path = Path('data/skills_taxonomy.json')
    
    resume_parser = ResumeParser()
    jd_parser = JDParser()
    extractor = KeywordExtractor(str(taxonomy_path))
    scorer = ResumeScorer(str(config_path) if config_path.exists() else None)
    
    MODULES_LOADED = True
except Exception as e:
    print(f"Warning: Could not load modules: {e}")
    MODULES_LOADED = False

DASHBOARD_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>SmartHire.AI</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px 40px;
            text-align: center;
        }
        .header h1 { font-size: 32px; margin-bottom: 10px; }
        .header p { opacity: 0.9; }
        
        .main { padding: 40px; }
        
        .section {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
        }
        .section h2 { margin-bottom: 20px; color: #333; }
        
        textarea {
            width: 100%;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 14px;
            font-family: inherit;
            min-height: 200px;
        }
        textarea:focus { outline: none; border-color: #667eea; }
        
        .upload-area {
            border: 3px dashed #667eea;
            border-radius: 15px;
            padding: 40px;
            text-align: center;
            background: white;
            cursor: pointer;
            transition: all 0.3s;
        }
        .upload-area:hover { background: #f0f4ff; }
        
        .file-list {
            margin-top: 20px;
            max-height: 200px;
            overflow-y: auto;
        }
        .file-item {
            background: white;
            padding: 10px 15px;
            border-radius: 8px;
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .settings {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        .settings input {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
        }
        
        .btn {
            padding: 15px 40px;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            transition: transform 0.2s;
        }
        .btn:hover { transform: translateY(-2px); }
        .btn:disabled { opacity: 0.6; cursor: not-allowed; }
        
        .progress {
            display: none;
            margin: 20px 0;
            text-align: center;
        }
        .progress-bar {
            width: 100%;
            height: 8px;
            background: #e0e0e0;
            border-radius: 10px;
            overflow: hidden;
            margin-bottom: 10px;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            width: 0%;
            transition: width 0.3s;
        }
        
        .results {
            display: none;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 10px;
            overflow: hidden;
        }
        th {
            background: #667eea;
            color: white;
            padding: 15px;
            text-align: left;
        }
        td {
            padding: 15px;
            border-bottom: 1px solid #e0e0e0;
        }
        tr:hover { background: #f8f9fa; }
        
        .score {
            font-weight: 600;
            padding: 5px 12px;
            border-radius: 20px;
            display: inline-block;
        }
        .score.high { background: #d4edda; color: #155724; }
        .score.medium { background: #fff3cd; color: #856404; }
        .score.low { background: #f8d7da; color: #721c24; }
        
        .alert {
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            display: none;
        }
        .alert.success { background: #d4edda; color: #155724; }
        .alert.error { background: #f8d7da; color: #721c24; }
        .alert.show { display: block; }
        
        .export-btns {
            margin: 20px 0;
            display: flex;
            gap: 10px;
        }
        .btn-export {
            padding: 10px 20px;
            background: white;
            border: 2px solid #667eea;
            color: #667eea;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
        }
        .btn-export:hover { background: #667eea; color: white; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 SmartHire.AI</h1>
            <p>Intelligent Resume Screening System</p>
        </div>

        <div class="main">
            <div class="alert" id="alert"></div>

            <div class="section">
                <h2>📝 Job Description</h2>
                <textarea id="jobDescription" placeholder="Paste your job description here...

Example:
Senior Python Developer

Required Skills:
- Python, Django, PostgreSQL
- Docker, Git

Preferred Skills:
- AWS, Kubernetes

Experience: 5+ years"></textarea>
            </div>

            <div class="section">
                <h2>📁 Upload Resumes</h2>
                <div class="upload-area" onclick="document.getElementById('fileInput').click()">
                    <div style="font-size: 48px; margin-bottom: 15px;">📤</div>
                    <div style="font-size: 16px; margin-bottom: 10px;">Click to upload resume files</div>
                    <div style="font-size: 13px; color: #999;">PDF and DOCX files supported</div>
                    <input type="file" id="fileInput" multiple accept=".pdf,.docx" style="display: none;">
                </div>
                <div class="file-list" id="fileList"></div>
            </div>

            <div class="section">
                <h2>⚙️ Settings</h2>
                <div class="settings">
                    <div>
                        <label>Top N Matches</label>
                        <input type="number" id="topN" value="10" min="1" max="100">
                    </div>
                    <div>
                        <label>Minimum Score (%)</label>
                        <input type="number" id="minScore" value="0" min="0" max="100">
                    </div>
                </div>
            </div>

            <div style="text-align: center;">
                <button class="btn" id="processBtn" onclick="process()">🚀 Start Screening</button>
            </div>

            <div class="progress" id="progress">
                <div class="progress-bar">
                    <div class="progress-fill" id="progressFill"></div>
                </div>
                <div id="progressText">Processing...</div>
            </div>

            <div class="results" id="results">
                <div class="section">
                    <h2>🏆 Results</h2>
                    <div class="export-btns">
                        <button class="btn-export" onclick="exportCSV()">📊 Export CSV</button>
                        <button class="btn-export" onclick="exportJSON()">📄 Export JSON</button>
                    </div>
                    <table id="resultsTable">
                        <thead>
                            <tr>
                                <th>Rank</th>
                                <th>Name</th>
                                <th>Email</th>
                                <th>Score</th>
                                <th>Experience</th>
                                <th>Skills</th>
                            </tr>
                        </thead>
                        <tbody id="resultsBody"></tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <script>
        let files = [];
        let resultsData = [];

        document.getElementById('fileInput').addEventListener('change', (e) => {
            files = Array.from(e.target.files);
            displayFiles();
        });

        function displayFiles() {
            const list = document.getElementById('fileList');
            list.innerHTML = files.map((f, i) => `
                <div class="file-item">
                    <span>📄 ${f.name}</span>
                    <button onclick="removeFile(${i})" style="background:#ff4757;color:white;border:none;padding:5px 12px;border-radius:5px;cursor:pointer;">Remove</button>
                </div>
            `).join('');
        }

        function removeFile(i) {
            files.splice(i, 1);
            displayFiles();
        }

        async function process() {
            const jd = document.getElementById('jobDescription').value.trim();
            const topN = parseInt(document.getElementById('topN').value);
            const minScore = parseFloat(document.getElementById('minScore').value);

            if (!jd) {
                showAlert('Please enter job description', 'error');
                return;
            }
            if (files.length === 0) {
                showAlert('Please upload resumes', 'error');
                return;
            }

            document.getElementById('processBtn').disabled = true;
            document.getElementById('progress').style.display = 'block';
            updateProgress(10, 'Uploading...');

            const formData = new FormData();
            files.forEach(f => formData.append('files', f));
            formData.append('job_description', jd);
            formData.append('top_n', topN);
            formData.append('min_score', minScore);

            try {
                updateProgress(50, 'Processing...');
                
                const response = await fetch('/process', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();

                if (data.success) {
                    updateProgress(100, 'Complete!');
                    resultsData = data.results;
                    displayResults(data.results);
                    showAlert(`Processed ${data.total} resumes successfully!`, 'success');
                } else {
                    throw new Error(data.message || 'Processing failed');
                }
            } catch (error) {
                showAlert('Error: ' + error.message, 'error');
            } finally {
                document.getElementById('processBtn').disabled = false;
                setTimeout(() => {
                    document.getElementById('progress').style.display = 'none';
                }, 2000);
            }
        }

        function updateProgress(percent, text) {
            document.getElementById('progressFill').style.width = percent + '%';
            document.getElementById('progressText').textContent = text;
        }

        function displayResults(results) {
            const tbody = document.getElementById('resultsBody');
            tbody.innerHTML = results.map((r, i) => {
                const scoreClass = r.total_score >= 80 ? 'high' : r.total_score >= 60 ? 'medium' : 'low';
                return `
                    <tr>
                        <td><strong>#${i + 1}</strong></td>
                        <td>${r.name}</td>
                        <td>${r.email || 'N/A'}</td>
                        <td><span class="score ${scoreClass}">${r.total_score.toFixed(1)}%</span></td>
                        <td>${r.experience_years} years</td>
                        <td>${r.matched_skills.slice(0, 3).join(', ')}</td>
                    </tr>
                `;
            }).join('');

            document.getElementById('results').style.display = 'block';
            document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
        }

        function exportCSV() {
            let csv = 'Rank,Name,Email,Score,Experience,Skills\\n';
            resultsData.forEach((r, i) => {
                csv += `${i+1},"${r.name}","${r.email}",${r.total_score},${r.experience_years},"${r.matched_skills.join(', ')}"\\n`;
            });
            download(csv, 'results.csv', 'text/csv');
        }

        function exportJSON() {
            download(JSON.stringify(resultsData, null, 2), 'results.json', 'application/json');
        }

        function download(content, filename, type) {
            const blob = new Blob([content], { type });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            a.click();
            URL.revokeObjectURL(url);
        }

        function showAlert(msg, type) {
            const alert = document.getElementById('alert');
            alert.textContent = msg;
            alert.className = `alert ${type} show`;
            setTimeout(() => alert.classList.remove('show'), 5000);
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(DASHBOARD_HTML)

@app.route('/process', methods=['POST'])
def process():
    try:
        if not MODULES_LOADED:
            return jsonify({"success": False, "message": "Modules not loaded"}), 500
        
        # Get files and parameters
        files = request.files.getlist('files')
        job_description = request.form.get('job_description')
        top_n = int(request.form.get('top_n', 10))
        min_score = float(request.form.get('min_score', 0))
        
        if not files or not job_description:
            return jsonify({"success": False, "message": "Missing files or job description"}), 400
        
        # Save files
        saved_files = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                saved_files.append(filepath)
        
        # Parse JD
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as tmp:
            tmp.write(job_description)
            tmp_path = tmp.name
        
        jd_data = jd_parser.parse_file(tmp_path)
        os.unlink(tmp_path)
        
        # Process resumes
        results = []
        for filepath in saved_files:
            try:
                resume = resume_parser.parse_file(filepath)
                skills = extractor.extract_skills(resume['text'])
                experience = extractor.extract_experience_years(resume['text'])
                keywords = extractor.extract_keywords(resume['text'])
                
                score = scorer.score_resume(skills, experience, keywords, jd_data)
                
                results.append({
                    'filename': os.path.basename(filepath),
                    'name': resume.get('name', 'Unknown'),
                    'email': resume.get('email', ''),
                    'phone': resume.get('phone', ''),
                    'total_score': score['total_score'],
                    'experience_years': score['resume_experience'],
                    'matched_skills': score['matched_required_skills'][:10],
                    'missing_skills': score['missing_required_skills'][:10]
                })
            except Exception as e:
                print(f"Error processing {filepath}: {e}")
        
        # Filter and sort
        if min_score > 0:
            results = [r for r in results if r['total_score'] >= min_score]
        
        results.sort(key=lambda x: x['total_score'], reverse=True)
        results = results[:top_n]
        
        # Cleanup
        for filepath in saved_files:
            try:
                os.unlink(filepath)
            except:
                pass
        
        return jsonify({
            "success": True,
            "total": len(saved_files),
            "results": results
        })
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("SmartHire.AI - YOUR COMPLETE PROJECT")
    print("="*60)
    print("Open: http://localhost:5000")
    print("="*60 + "\n")
    app.run(host='0.0.0.0', port=5000, debug=True)
