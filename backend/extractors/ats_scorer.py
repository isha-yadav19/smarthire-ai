"""
SmartHire.AI - ATS (Applicant Tracking System) Scorer
Evaluates resume formatting and ATS-friendliness
"""

import re
from pathlib import Path

class ATSScorer:
    """Scores resume based on ATS compatibility"""
    
    def __init__(self):
        self.standard_sections = [
            'experience', 'education', 'skills', 'summary',
            'work experience', 'professional experience',
            'qualifications', 'certifications', 'projects'
        ]
    
    def score_resume(self, resume_text, file_path=None):
        """
        Calculate ATS score (0-100)
        
        Criteria:
        - Has contact information (20 points)
        - Has standard sections (30 points)
        - Proper formatting (20 points)
        - No complex elements (15 points)
        - Keyword density (15 points)
        """
        score = 0
        issues = []
        
        # 1. Contact Information (20 points)
        contact_score = self._check_contact_info(resume_text)
        score += contact_score
        if contact_score < 20:
            issues.append("Missing or incomplete contact information")
        
        # 2. Standard Sections (30 points)
        section_score = self._check_sections(resume_text)
        score += section_score
        if section_score < 20:
            issues.append("Missing standard resume sections")
        
        # 3. Proper Formatting (20 points)
        format_score = self._check_formatting(resume_text)
        score += format_score
        if format_score < 15:
            issues.append("Formatting issues detected")
        
        # 4. No Complex Elements (15 points)
        complexity_score = self._check_complexity(resume_text, file_path)
        score += complexity_score
        if complexity_score < 10:
            issues.append("Contains complex formatting elements")
        
        # 5. Keyword Density (15 points)
        keyword_score = self._check_keyword_density(resume_text)
        score += keyword_score
        if keyword_score < 10:
            issues.append("Low keyword density")
        
        return {
            'ats_score': min(score, 100),
            'contact_score': contact_score,
            'section_score': section_score,
            'format_score': format_score,
            'complexity_score': complexity_score,
            'keyword_score': keyword_score,
            'issues': issues,
            'recommendations': self._generate_recommendations(issues)
        }
    
    def _check_contact_info(self, text):
        """Check for email, phone, name (20 points max)"""
        score = 0
        
        # Email (8 points)
        if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text):
            score += 8
        
        # Phone (7 points)
        if re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text):
            score += 7
        
        # Name at top (5 points) - check if first 200 chars have capitalized words
        first_lines = text[:200]
        if re.search(r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b', first_lines):
            score += 5
        
        return score
    
    def _check_sections(self, text):
        """Check for standard resume sections (30 points max)"""
        text_lower = text.lower()
        found_sections = 0
        
        for section in self.standard_sections:
            # Look for section headers (bold, caps, or followed by colon)
            pattern = rf'\b{section}\b'
            if re.search(pattern, text_lower):
                found_sections += 1
        
        # Score based on number of sections found
        if found_sections >= 4:
            return 30
        elif found_sections == 3:
            return 25
        elif found_sections == 2:
            return 15
        elif found_sections == 1:
            return 10
        else:
            return 0
    
    def _check_formatting(self, text):
        """Check formatting quality (20 points max)"""
        score = 20
        
        # Check for excessive special characters
        special_chars = len(re.findall(r'[^\w\s\-.,()@]', text))
        if special_chars > 50:
            score -= 5
        
        # Check for proper capitalization
        sentences = text.split('.')
        properly_capitalized = sum(1 for s in sentences if s.strip() and s.strip()[0].isupper())
        if properly_capitalized < len(sentences) * 0.7:
            score -= 5
        
        # Check for reasonable line length (not too long)
        lines = text.split('\n')
        long_lines = sum(1 for line in lines if len(line) > 120)
        if long_lines > len(lines) * 0.3:
            score -= 5
        
        # Check for bullet points or lists
        if re.search(r'[•\-\*]\s', text):
            score += 5  # Bonus for using lists
        
        return max(score, 0)
    
    def _check_complexity(self, text, file_path):
        """Check for complex elements that ATS might struggle with (15 points max)"""
        score = 15
        
        # Check for table-like structures
        if re.search(r'\|.*\|.*\|', text):
            score -= 5
        
        # Check for excessive whitespace (might indicate columns)
        lines = text.split('\n')
        whitespace_heavy = sum(1 for line in lines if line.count('  ') > 3)
        if whitespace_heavy > len(lines) * 0.2:
            score -= 3
        
        # Check for very short lines (might indicate complex layout)
        very_short = sum(1 for line in lines if 0 < len(line.strip()) < 10)
        if very_short > len(lines) * 0.3:
            score -= 3
        
        # Bonus for clean text
        if len(text) > 500 and score == 15:
            score += 0  # Keep at 15
        
        return max(score, 0)
    
    def _check_keyword_density(self, text):
        """Check for appropriate keyword usage (15 points max)"""
        words = text.lower().split()
        total_words = len(words)
        
        if total_words == 0:
            return 0
        
        # Common professional keywords
        keywords = [
            'experience', 'developed', 'managed', 'led', 'created',
            'implemented', 'designed', 'analyzed', 'improved', 'achieved',
            'project', 'team', 'client', 'business', 'technical'
        ]
        
        keyword_count = sum(1 for word in words if word in keywords)
        keyword_ratio = keyword_count / total_words
        
        # Optimal ratio: 5-15%
        if 0.05 <= keyword_ratio <= 0.15:
            return 15
        elif 0.03 <= keyword_ratio < 0.05 or 0.15 < keyword_ratio <= 0.20:
            return 10
        elif keyword_ratio > 0:
            return 5
        else:
            return 0
    
    def _generate_recommendations(self, issues):
        """Generate actionable recommendations"""
        recommendations = []
        
        if "Missing or incomplete contact information" in issues:
            recommendations.append("Add clear contact information at the top: name, email, phone number")
        
        if "Missing standard resume sections" in issues:
            recommendations.append("Include standard sections: Experience, Education, Skills")
        
        if "Formatting issues detected" in issues:
            recommendations.append("Use consistent formatting with proper capitalization and bullet points")
        
        if "Contains complex formatting elements" in issues:
            recommendations.append("Avoid tables, columns, and complex layouts - use simple linear format")
        
        if "Low keyword density" in issues:
            recommendations.append("Include more action verbs and industry-specific keywords")
        
        return recommendations


# Test ATS Scorer
if __name__ == "__main__":
    scorer = ATSScorer()
    
    # Test with sample resume text
    sample_resume = """
    John Doe
    john.doe@email.com | (555) 123-4567
    
    PROFESSIONAL SUMMARY
    Experienced software developer with 5+ years in Python development.
    
    EXPERIENCE
    Senior Developer at Tech Corp (2020-Present)
    - Developed microservices using Python and Django
    - Led team of 5 developers
    - Implemented CI/CD pipelines
    
    EDUCATION
    BS Computer Science, University of Technology (2018)
    
    SKILLS
    Python, Django, AWS, Docker, Kubernetes
    """
    
    result = scorer.score_resume(sample_resume)
    
    print("ATS Scoring Results:")
    print("=" * 50)
    print(f"Overall ATS Score: {result['ats_score']}/100")
    print(f"\nBreakdown:")
    print(f"  Contact Info: {result['contact_score']}/20")
    print(f"  Sections: {result['section_score']}/30")
    print(f"  Formatting: {result['format_score']}/20")
    print(f"  Complexity: {result['complexity_score']}/15")
    print(f"  Keywords: {result['keyword_score']}/15")
    
    if result['issues']:
        print(f"\nIssues Found:")
        for issue in result['issues']:
            print(f"  - {issue}")
    
    if result['recommendations']:
        print(f"\nRecommendations:")
        for rec in result['recommendations']:
            print(f"  • {rec}")
