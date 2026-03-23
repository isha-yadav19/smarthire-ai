"""
SmartHire.AI - Database Connection Module
PostgreSQL connection and query utilities
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        """Initialize database connection"""
        self.conn = None
        self.connect()
    
    def connect(self):
        """Establish connection to PostgreSQL"""
        try:
            self.conn = psycopg2.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                port=os.getenv('DB_PORT', '5432'),
                database=os.getenv('DB_NAME', 'smarthire_db'),
                user=os.getenv('DB_USER', 'postgres'),
                password=os.getenv('DB_PASSWORD', 'postgres')
            )
            print("✅ Database connected successfully!")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            raise
    
    def execute_query(self, query, params=None, fetch=True):
        """Execute SQL query"""
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params)
                if fetch:
                    return cursor.fetchall()
                self.conn.commit()
                return cursor.rowcount
        except Exception as e:
            self.conn.rollback()
            print(f"Query error: {e}")
            raise
    
    def insert_user(self, username, email, password_hash, role):
        """Insert new user"""
        query = """
            INSERT INTO users (username, email, password_hash, role)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """
        result = self.execute_query(query, (username, email, password_hash, role))
        return result[0]['id'] if result else None
    
    def get_user_by_username(self, username):
        """Get user by username"""
        query = "SELECT * FROM users WHERE username = %s"
        result = self.execute_query(query, (username,))
        return result[0] if result else None
    
    def insert_candidate(self, name, email, mobile, resume_filename, resume_text, skills, experience_years, uploaded_by):
        """Insert candidate"""
        query = """
            INSERT INTO candidates (name, email, mobile, resume_filename, resume_text, skills, experience_years, uploaded_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        result = self.execute_query(query, (name, email, mobile, resume_filename, resume_text, skills, experience_years, uploaded_by))
        return result[0]['id'] if result else None
    
    def get_all_candidates(self):
        """Get all candidates"""
        query = "SELECT * FROM candidates ORDER BY uploaded_at DESC"
        return self.execute_query(query)
    
    def insert_job_posting(self, title, description, required_skills, preferred_skills, experience_required, department, created_by):
        """Insert job posting"""
        query = """
            INSERT INTO job_postings (title, description_text, required_skills, preferred_skills, experience_required, department, created_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        result = self.execute_query(query, (title, description, required_skills, preferred_skills, experience_required, department, created_by))
        return result[0]['id'] if result else None
    
    def get_all_jobs(self, status='open'):
        """Get all job postings"""
        query = "SELECT * FROM job_postings WHERE status = %s ORDER BY created_at DESC"
        return self.execute_query(query, (status,))
    
    def insert_screening_result(self, job_id, candidate_id, scores, matched_skills, missing_skills, screened_by):
        """Insert screening result"""
        query = """
            INSERT INTO screening_results (
                job_posting_id, candidate_id, total_score, required_skills_score,
                preferred_skills_score, experience_score, keywords_score,
                ats_score, semantic_similarity_score, matched_skills, missing_skills, screened_by
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        result = self.execute_query(query, (
            job_id, candidate_id, scores['total'], scores['required_skills'],
            scores['preferred_skills'], scores['experience'], scores['keywords'],
            scores['ats'], scores['semantic'], matched_skills, missing_skills, screened_by
        ))
        return result[0]['id'] if result else None
    
    def get_screening_results(self, job_id):
        """Get screening results for a job"""
        query = """
            SELECT sr.*, c.name, c.email, c.mobile
            FROM screening_results sr
            JOIN candidates c ON sr.candidate_id = c.id
            WHERE sr.job_posting_id = %s
            ORDER BY sr.total_score DESC
        """
        return self.execute_query(query, (job_id,))
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("Database connection closed")

# Test connection
if __name__ == "__main__":
    db = Database()
    print("Testing database connection...")
    users = db.execute_query("SELECT * FROM users")
    print(f"Found {len(users)} users in database")
    for user in users:
        print(f"  - {user['username']} ({user['role']})")
    db.close()
