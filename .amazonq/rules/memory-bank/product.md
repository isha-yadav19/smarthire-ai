# Product Overview

## Purpose
Resume Screening System is an intelligent, automated recruitment tool that processes large volumes of resumes (500-1000+) against job descriptions to rank candidates based on skills match, experience, and relevance. Built for HR professionals and recruitment teams to streamline candidate evaluation.

## Core Value Proposition
- Eliminates manual resume screening bottlenecks
- Provides objective, data-driven candidate rankings
- Reduces time-to-hire through batch processing
- Ensures consistent evaluation criteria across all candidates

## Key Features

### Resume Processing
- **Multi-format support**: Parses PDF and DOCX resumes automatically
- **Batch processing**: Handles 500-1000 resumes simultaneously
- **Contact extraction**: Automatically extracts names, emails, phone numbers
- **Text extraction**: Robust parsing from various resume formats

### Intelligent Matching
- **Weighted scoring algorithm**: Configurable weights for different criteria
  - Required Skills: 40%
  - Preferred Skills: 20%
  - Experience: 15%
  - Keyword Density: 10%
  - ATS Score: 5%
  - Semantic Similarity: 10%
- **Skills taxonomy**: 1000+ technical and soft skills database
- **Experience matching**: Years of experience calculation and tolerance
- **Keyword relevance**: Frequency analysis of job-specific terms

### User Interfaces
- **Web interface**: Streamlit-based UI for easy interaction
- **CLI mode**: Command-line processing for automation
- **REST API**: Flask-based API server for integration

### Output & Export
- **Multiple formats**: CSV, JSON, JSONL exports
- **Bulk downloads**: ZIP archives of top-ranked resumes
- **Individual access**: Direct download links for each candidate
- **Detailed scoring**: Breakdown by category (skills, experience, keywords)

### Advanced Features
- **ATS scoring**: Applicant Tracking System compatibility analysis
- **Skill gap analysis**: Identifies missing skills for each candidate
- **Course recommendations**: Suggests training based on skill gaps
- **Database integration**: PostgreSQL storage for results and analytics
- **Authentication**: Secure login system with bcrypt encryption

## Target Users
- HR professionals managing high-volume recruitment
- Recruitment agencies screening multiple candidates
- Hiring managers evaluating technical positions
- Talent acquisition teams needing objective rankings

## Use Cases
1. **High-volume hiring**: Process hundreds of applications for open positions
2. **Technical recruitment**: Match candidates against specific tech stacks
3. **Skill-based filtering**: Identify candidates with required competencies
4. **Experience screening**: Filter by years of experience with tolerance
5. **Batch evaluation**: Consistent scoring across large candidate pools
6. **Resume analytics**: Track candidate quality and skill distributions
