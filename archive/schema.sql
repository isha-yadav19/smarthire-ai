-- SmartHire.AI Database Schema
-- PostgreSQL 15+

DROP TABLE IF EXISTS learning_recommendations CASCADE;
DROP TABLE IF EXISTS screening_results CASCADE;
DROP TABLE IF EXISTS job_postings CASCADE;
DROP TABLE IF EXISTS candidates CASCADE;
DROP TABLE IF EXISTS users CASCADE;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) CHECK (role IN ('admin', 'recruiter')) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);

CREATE TABLE candidates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200),
    email VARCHAR(100),
    mobile VARCHAR(20),
    resume_filename VARCHAR(255) NOT NULL,
    resume_text TEXT,
    skills JSONB,
    experience_years INTEGER,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    uploaded_by INTEGER REFERENCES users(id) ON DELETE SET NULL
);

CREATE INDEX idx_candidates_name ON candidates(name);
CREATE INDEX idx_candidates_email ON candidates(email);
CREATE INDEX idx_candidates_skills ON candidates USING GIN(skills);

CREATE TABLE job_postings (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description_text TEXT,
    required_skills JSONB,
    preferred_skills JSONB,
    experience_required INTEGER,
    department VARCHAR(100),
    status VARCHAR(20) DEFAULT 'open' CHECK (status IN ('open', 'closed')),
    created_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_job_postings_status ON job_postings(status);

CREATE TABLE screening_results (
    id SERIAL PRIMARY KEY,
    job_posting_id INTEGER REFERENCES job_postings(id) ON DELETE CASCADE,
    candidate_id INTEGER REFERENCES candidates(id) ON DELETE CASCADE,
    total_score DECIMAL(5,2),
    required_skills_score DECIMAL(5,2),
    preferred_skills_score DECIMAL(5,2),
    experience_score DECIMAL(5,2),
    keywords_score DECIMAL(5,2),
    ats_score DECIMAL(5,2),
    semantic_similarity_score DECIMAL(5,2),
    matched_skills JSONB,
    missing_skills JSONB,
    screened_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    screened_by INTEGER REFERENCES users(id) ON DELETE SET NULL
);

CREATE INDEX idx_screening_score ON screening_results(total_score DESC);

CREATE TABLE learning_recommendations (
    id SERIAL PRIMARY KEY,
    candidate_id INTEGER REFERENCES candidates(id) ON DELETE CASCADE,
    job_posting_id INTEGER REFERENCES job_postings(id) ON DELETE CASCADE,
    missing_skill VARCHAR(100) NOT NULL,
    recommended_course VARCHAR(255),
    course_url TEXT,
    priority VARCHAR(20) CHECK (priority IN ('high', 'medium', 'low')) DEFAULT 'medium',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (username, email, password_hash, role) VALUES
('admin', 'admin@smarthire.ai', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIvAprzZ3i', 'admin'),
('recruiter1', 'recruiter1@smarthire.ai', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIvAprzZ3i', 'recruiter');
