"""
SmartHire.AI - Recruiter Dashboard
Simplified interface for recruiters to screen candidates
"""

import streamlit as st
import tempfile
import shutil
from pathlib import Path
import pandas as pd
from datetime import datetime
import io
import zipfile
import json

from parsers import ResumeParser, JDParser
from extractors import KeywordExtractor, ATSScorer, SkillGapAnalyzer
from matcher import ResumeScorer

# Page configuration
st.set_page_config(
    page_title="SmartHire.AI - Recruiter Portal",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Recruiter Theme
st.markdown("""
    <style>
    :root {
        --primary-color: #C9A84C;
        --secondary-color: #1A2332;
    }
    
    .main-header {
        font-family: 'Playfair Display', serif;
        font-size: 2.2rem;
        font-weight: 700;
        color: #1A2332;
        margin-bottom: 0.5rem;
    }
    
    .recruiter-badge {
        background: linear-gradient(135deg, #C9A84C 0%, #B8973D 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    .badge-title {
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.25rem;
    }
    
    .badge-role {
        font-size: 0.85rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton>button {
        background: #C9A84C;
        color: white;
        font-weight: 500;
        border-radius: 8px;
        border: none;
        padding: 0.75rem 2rem;
    }
    
    .stButton>button:hover {
        background: #B8973D;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(201, 168, 76, 0.3);
    }
    
    div[data-testid="stMetricValue"] {
        color: #C9A84C;
        font-size: 1.8rem;
        font-weight: 700;
    }
    
    .section-header {
        font-size: 1.3rem;
        font-weight: 600;
        color: #1A2332;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #C9A84C;
    }
    
    .quick-tip {
        background: #FEF3C7;
        border-left: 4px solid #C9A84C;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-size: 0.9rem;
    }
    
    .candidate-card {
        background: #F9FAFB;
        border: 1px solid #E5E7EB;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.5rem;
    }
    </style>
    
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)


@st.cache_resource
def load_components():
    """Load system components"""
    config_path = Path(__file__).parent / 'data' / 'config.json'
    taxonomy_path = Path(__file__).parent / 'data' / 'skills_taxonomy.json'
    courses_path = Path(__file__).parent / 'data' / 'courses.json'
    
    resume_parser = ResumeParser()
    jd_parser = JDParser()
    extractor = KeywordExtractor(str(taxonomy_path))
    scorer = ResumeScorer(str(config_path) if config_path.exists() else None)
    ats_scorer = ATSScorer()
    skill_gap_analyzer = SkillGapAnalyzer(str(courses_path))
    
    return resume_parser, jd_parser, extractor, scorer, ats_scorer, skill_gap_analyzer


def process_resumes(resume_files, jd_data, top_n, min_score, resume_parser, extractor, scorer, ats_scorer, skill_gap_analyzer):
    """Process resumes with progress tracking"""
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Upload files
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text(f"📤 Uploading {len(resume_files)} files...")
        temp_files = []
        file_mapping = {}
        
        for idx, uploaded_file in enumerate(resume_files):
            file_path = Path(temp_dir) / uploaded_file.name
            with open(file_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            temp_files.append(file_path)
            file_mapping[str(file_path)] = uploaded_file
            progress_bar.progress((idx + 1) / (len(resume_files) * 3))
        
        # Parse resumes
        status_text.text("📄 Parsing resumes...")
        resumes = []
        
        for idx, file_path in enumerate(temp_files):
            try:
                resume = resume_parser.parse_file(str(file_path))
                resume['filename'] = file_path.name
                resume['file_object'] = file_mapping[str(file_path)]
                resumes.append(resume)
            except Exception as e:
                st.warning(f"⚠️ Skipped {file_path.name}: {str(e)}")
            progress_bar.progress((len(resume_files) + idx + 1) / (len(resume_files) * 3))
        
        if not resumes:
            st.error("❌ No resumes could be parsed")
            return None
        
        # Score resumes
        status_text.text(f"🎯 Scoring {len(resumes)} candidates...")
        scored_resumes = []
        
        for idx, resume in enumerate(resumes):
            resume_skills = extractor.extract_skills(resume['text'])
            resume_experience = extractor.extract_experience_years(resume['text'])
            resume_keywords = extractor.extract_keywords(resume['text'])
            
            score = scorer.score_resume(resume_skills, resume_experience, resume_keywords, jd_data)
            ats_result = ats_scorer.score_resume(resume['text'])
            skill_gap = skill_gap_analyzer.analyze_gap(
                list(resume_skills),
                list(jd_data['required_skills']),
                list(jd_data['preferred_skills'])
            )
            
            scored_resumes.append({
                'resume': resume,
                'score': score,
                'skills': list(resume_skills),
                'experience': resume_experience,
                'ats_score': ats_result['ats_score'],
                'skill_gap': skill_gap
            })
            progress_bar.progress((len(resume_files) * 2 + idx + 1) / (len(resume_files) * 3))
        
        status_text.text("✅ Processing complete!")
        progress_bar.progress(1.0)
        
        # Filter and rank
        if min_score:
            scored_resumes = [r for r in scored_resumes if r['score']['total_score'] >= min_score]
        
        ranked_resumes = sorted(scored_resumes, key=lambda x: x['score']['total_score'], reverse=True)
        return ranked_resumes[:top_n]
        
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def main():
    """Recruiter Dashboard"""
    
    # Header
    col_h1, col_h2 = st.columns([3, 1])
    
    with col_h1:
        st.markdown('<h1 class="main-header">🎯 SmartHire.AI - Recruiter Portal</h1>', unsafe_allow_html=True)
    
    with col_h2:
        st.markdown("""
            <div class="recruiter-badge">
                <div class="badge-title">Recruiter Dashboard</div>
                <div class="badge-role">Talent Screening</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Load components
    with st.spinner("⚙️ Loading system..."):
        resume_parser, jd_parser, extractor, scorer, ats_scorer, skill_gap_analyzer = load_components()
    
    # Tabs for different functions
    tab1, tab2 = st.tabs(["📝 Post Job", "📋 Screen Candidates"])
    
    # TAB 1: POST JOB
    with tab1:
        st.markdown('<div class="section-header">📝 Post New Job</div>', unsafe_allow_html=True)
        
        col_p1, col_p2 = st.columns(2)
        
        with col_p1:
            company_name = st.text_input("Company Name", placeholder="e.g., Tech Corp")
            job_title = st.text_input("Job Title", placeholder="e.g., Senior Python Developer")
            location = st.text_input("Location", placeholder="e.g., San Francisco, CA")
            job_type = st.selectbox("Job Type", ["Full-time", "Part-time", "Contract", "Remote"])
        
        with col_p2:
            salary = st.text_input("Salary Range", placeholder="e.g., $100k - $140k")
            experience = st.number_input("Years of Experience", min_value=0, max_value=20, value=3)
            required_skills = st.text_input("Required Skills (comma-separated)", placeholder="Python, Django, PostgreSQL")
            preferred_skills = st.text_input("Preferred Skills (comma-separated)", placeholder="AWS, Docker, Kubernetes")
        
        if st.button("📤 Post Job", type="primary", use_container_width=True):
            if company_name and job_title and required_skills:
                # Load existing jobs
                jobs_file = Path(__file__).parent / 'data' / 'jobs.json'
                
                if jobs_file.exists():
                    with open(jobs_file, 'r') as f:
                        jobs_data = json.load(f)
                else:
                    jobs_data = {"jobs": []}
                
                # Create new job
                new_job = {
                    "id": len(jobs_data['jobs']) + 1,
                    "company": company_name,
                    "title": job_title,
                    "location": location,
                    "type": job_type,
                    "salary": salary,
                    "required_skills": [s.strip() for s in required_skills.split(',')],
                    "preferred_skills": [s.strip() for s in preferred_skills.split(',')] if preferred_skills else [],
                    "experience": experience,
                    "posted_date": datetime.now().strftime("%Y-%m-%d")
                }
                
                jobs_data['jobs'].append(new_job)
                
                # Save to file
                jobs_file.parent.mkdir(exist_ok=True)
                with open(jobs_file, 'w') as f:
                    json.dump(jobs_data, f, indent=2)
                
                st.success(f"✅ Job posted successfully! Job ID: {new_job['id']}")
                st.balloons()
            else:
                st.error("❌ Please fill in Company Name, Job Title, and Required Skills")
    
    # TAB 2: SCREEN CANDIDATES
    with tab2:
        # Sidebar
        st.sidebar.header("⚙️ Screening Settings")
        
        top_n = st.sidebar.slider(
            "Number of Top Candidates",
            min_value=5,
            max_value=50,
            value=10,
            step=5,
            help="How many top candidates to show"
        )
        
        min_score = st.sidebar.slider(
            "Minimum Match Score (%)",
            min_value=0,
            max_value=100,
            value=50,
            step=5,
            help="Filter candidates below this score"
        )
        
        if min_score == 0:
            min_score = None
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📊 Scoring Criteria")
        st.sidebar.info("""
    **Required Skills**: 40%  
    **Preferred Skills**: 20%  
    **Experience**: 15%  
    **Keywords**: 10%  
    **ATS Score**: 5%  
    **Semantic Match**: 10%
        """)
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 💡 Quick Tips")
        st.sidebar.success("""
    ✅ Upload 10-500 resumes  
    ✅ Use PDF or DOCX format  
    ✅ Clear job requirements  
    ✅ Review top 10 candidates
        """)
        
        # Main content
        st.markdown('<div class="section-header">📋 Step 1: Job Requirements</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        jd_text = st.text_area(
            "Paste Job Description:",
            height=250,
            placeholder="""Example:

Senior Software Engineer

Required Skills:
- Python, Django, REST APIs
- PostgreSQL, Redis
- Docker, Kubernetes
- 5+ years experience

Preferred Skills:
- AWS, Terraform
- React, TypeScript
- CI/CD pipelines
""",
            help="Include required skills, preferred skills, and experience"
        )
    
    with col2:
        st.markdown("**📝 Job Description Tips:**")
        st.markdown("""
        1. List **Required Skills** clearly
        2. Separate **Preferred Skills**
        3. Mention **Years of Experience**
        4. Include specific technologies
        5. Add relevant keywords
        """)
        
        st.markdown("**🎯 Example Format:**")
        st.code("""Required Skills:
- Skill 1, Skill 2
- Technology A, B

Preferred Skills:
- Skill 3, Skill 4

Experience: X+ years""", language="text")
    
    jd_data = None
    if jd_text:
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as tmp:
                tmp.write(jd_text)
                tmp_path = tmp.name
            
            jd_data = jd_parser.parse_file(tmp_path)
            Path(tmp_path).unlink()
            
            col_jd1, col_jd2, col_jd3 = st.columns(3)
            with col_jd1:
                st.metric("✅ Required Skills", len(jd_data['required_skills']))
            with col_jd2:
                st.metric("⭐ Preferred Skills", len(jd_data['preferred_skills']))
            with col_jd3:
                st.metric("📅 Min Experience", f"{jd_data['min_experience']} yrs")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    # Resume upload
    st.markdown('<div class="section-header">📁 Step 2: Upload Resumes</div>', unsafe_allow_html=True)
    
    resume_files = st.file_uploader(
        "Upload Candidate Resumes (PDF/DOCX):",
        type=['pdf', 'docx'],
        accept_multiple_files=True,
        help="Select multiple resume files - supports up to 500 files"
    )
    
    if resume_files:
        st.success(f"✅ {len(resume_files)} resumes uploaded")
        
        if len(resume_files) > 20:
            with st.expander(f"📄 View Files ({len(resume_files)} total)"):
                for idx, file in enumerate(resume_files[:20], 1):
                    st.text(f"{idx}. {file.name}")
                st.text(f"... and {len(resume_files) - 20} more")
    
    # Process button
    st.markdown("---")
    
    if st.button("🚀 Start Candidate Screening", type="primary", use_container_width=True):
        if not jd_data:
            st.error("❌ Please enter job description first")
        elif not resume_files:
            st.error("❌ Please upload resume files")
        else:
            st.markdown('<div class="section-header">⚙️ Processing Candidates</div>', unsafe_allow_html=True)
            
            start_time = datetime.now()
            
            results = process_resumes(
                resume_files, jd_data, top_n, min_score,
                resume_parser, extractor, scorer, ats_scorer, skill_gap_analyzer
            )
            
            if results:
                processing_time = (datetime.now() - start_time).total_seconds()
                
                st.success(f"✅ Screening completed in {processing_time:.1f} seconds!")
                st.markdown("---")
                
                # Results
                st.markdown('<div class="section-header">🏆 Top Candidates</div>', unsafe_allow_html=True)
                
                # Metrics
                col_m1, col_m2, col_m3, col_m4 = st.columns(4)
                with col_m1:
                    st.metric("📊 Processed", len(resume_files))
                with col_m2:
                    st.metric("🎯 Qualified", len(results))
                with col_m3:
                    avg_score = sum([r['score']['total_score'] for r in results]) / len(results)
                    st.metric("📈 Avg Score", f"{avg_score:.0f}%")
                with col_m4:
                    st.metric("⭐ Top Score", f"{results[0]['score']['total_score']:.0f}%")
                
                # Candidate list
                st.markdown("### 📋 Ranked Candidates")
                
                for idx, result in enumerate(results, 1):
                    with st.expander(
                        f"#{idx} - {result['resume'].get('name', 'Unknown')} | "
                        f"Match: {result['score']['total_score']:.0f}% | "
                        f"ATS: {result['ats_score']}/100 | "
                        f"Exp: {result['experience']} yrs",
                        expanded=(idx <= 3)
                    ):
                        col_c1, col_c2 = st.columns([1, 1])
                        
                        with col_c1:
                            st.markdown("**👤 Contact**")
                            st.write(f"**Name:** {result['resume'].get('name', 'N/A')}")
                            st.write(f"**Email:** {result['resume'].get('email', 'N/A')}")
                            st.write(f"**Phone:** {result['resume'].get('phone', 'N/A')}")
                            
                            st.markdown("**📊 Scores**")
                            st.write(f"Match Score: {result['score']['total_score']:.1f}%")
                            st.write(f"ATS Score: {result['ats_score']}/100")
                            st.write(f"Experience: {result['experience']} years")
                        
                        with col_c2:
                            st.markdown("**✅ Matched Skills**")
                            matched = result['score']['matched_required_skills']
                            if matched:
                                st.success(", ".join(matched[:10]))
                            else:
                                st.info("No matches")
                            
                            st.markdown("**❌ Missing Skills**")
                            missing = result['skill_gap']['missing_required_skills']
                            if missing:
                                st.warning(", ".join(missing[:10]))
                            else:
                                st.success("None")
                        
                        # Download button
                        if 'file_object' in result['resume']:
                            st.download_button(
                                label="📥 Download Resume",
                                data=result['resume']['file_object'].getvalue(),
                                file_name=result['resume']['filename'],
                                mime="application/octet-stream",
                                key=f"dl_{idx}"
                            )
                
                # Export options
                st.markdown("---")
                st.markdown("### 📤 Export Results")
                
                col_e1, col_e2, col_e3 = st.columns(3)
                
                with col_e1:
                    # CSV export
                    data = []
                    for rank, r in enumerate(results, 1):
                        data.append({
                            'Rank': rank,
                            'Name': r['resume'].get('name', 'Unknown'),
                            'Email': r['resume'].get('email', ''),
                            'Phone': r['resume'].get('phone', ''),
                            'Match_Score': f"{r['score']['total_score']:.1f}",
                            'ATS_Score': r['ats_score'],
                            'Experience': r['experience'],
                            'Matched_Skills': ', '.join(r['score']['matched_required_skills']),
                            'Missing_Skills': ', '.join(r['skill_gap']['missing_required_skills'])
                        })
                    
                    df = pd.DataFrame(data)
                    csv = df.to_csv(index=False)
                    
                    st.download_button(
                        label="📊 Download CSV",
                        data=csv,
                        file_name=f"candidates_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                
                with col_e2:
                    # JSON export
                    json_data = df.to_json(orient='records', indent=2)
                    st.download_button(
                        label="📋 Download JSON",
                        data=json_data,
                        file_name=f"candidates_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json",
                        use_container_width=True
                    )
                
                with col_e3:
                    # ZIP of top resumes
                    zip_buffer = io.BytesIO()
                    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                        for idx, r in enumerate(results, 1):
                            if 'file_object' in r['resume']:
                                filename = f"{idx:02d}_{r['resume']['filename']}"
                                zip_file.writestr(filename, r['resume']['file_object'].getvalue())
                    
                    st.download_button(
                        label="📦 Download All Resumes",
                        data=zip_buffer.getvalue(),
                        file_name=f"top_candidates_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                        mime="application/zip",
                        use_container_width=True
                    )


if __name__ == "__main__":
    main()
