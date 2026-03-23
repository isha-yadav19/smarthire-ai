"""
SmartHire.AI - Skill Gap Analyzer
Identifies missing skills and recommends courses
"""

import json
from pathlib import Path

class SkillGapAnalyzer:
    """Analyzes skill gaps and recommends learning paths"""
    
    def __init__(self, courses_path=None):
        if courses_path is None:
            courses_path = Path(__file__).parent.parent / 'data' / 'courses.json'
        
        with open(courses_path, 'r') as f:
            self.courses_db = json.load(f)['courses']
    
    def analyze_gap(self, candidate_skills, required_skills, preferred_skills=None):
        """
        Analyze skill gap and generate recommendations
        
        Args:
            candidate_skills: Set of skills candidate has
            required_skills: Set of required skills for job
            preferred_skills: Set of preferred skills (optional)
        
        Returns:
            Dictionary with gap analysis and course recommendations
        """
        if preferred_skills is None:
            preferred_skills = set()
        
        # Convert to sets for easier operations
        candidate_skills = set(candidate_skills)
        required_skills = set(required_skills)
        preferred_skills = set(preferred_skills)
        
        # Identify gaps
        missing_required = required_skills - candidate_skills
        missing_preferred = preferred_skills - candidate_skills
        matched_required = required_skills & candidate_skills
        matched_preferred = preferred_skills & candidate_skills
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            missing_required, 
            missing_preferred
        )
        
        # Calculate learning time
        total_hours = sum(rec['estimated_hours'] for rec in recommendations)
        
        # Prioritize recommendations
        high_priority = [r for r in recommendations if r['priority'] == 'high']
        medium_priority = [r for r in recommendations if r['priority'] == 'medium']
        low_priority = [r for r in recommendations if r['priority'] == 'low']
        
        return {
            'matched_required_skills': list(matched_required),
            'matched_preferred_skills': list(matched_preferred),
            'missing_required_skills': list(missing_required),
            'missing_preferred_skills': list(missing_preferred),
            'match_percentage': self._calculate_match_percentage(
                len(matched_required), 
                len(required_skills)
            ),
            'recommendations': recommendations,
            'high_priority_courses': high_priority,
            'medium_priority_courses': medium_priority,
            'low_priority_courses': low_priority,
            'total_learning_hours': total_hours,
            'estimated_weeks': self._estimate_weeks(total_hours),
            'readiness_score': self._calculate_readiness(
                len(matched_required),
                len(required_skills),
                len(matched_preferred),
                len(preferred_skills)
            )
        }
    
    def _generate_recommendations(self, missing_required, missing_preferred):
        """Generate course recommendations for missing skills"""
        recommendations = []
        
        # Process required skills (high priority)
        for skill in missing_required:
            courses = self._find_courses(skill)
            if courses:
                # Take the first (usually best) course
                course = courses[0]
                recommendations.append({
                    'skill': skill,
                    'type': 'required',
                    'priority': 'high',
                    'course_title': course['title'],
                    'provider': course['provider'],
                    'duration': course['duration'],
                    'level': course['level'],
                    'url': course.get('url', ''),
                    'estimated_hours': self._parse_duration(course['duration'])
                })
            else:
                # No specific course found, add generic recommendation
                recommendations.append({
                    'skill': skill,
                    'type': 'required',
                    'priority': 'high',
                    'course_title': f'Learn {skill}',
                    'provider': 'Various',
                    'duration': 'Self-paced',
                    'level': 'Beginner',
                    'url': f'https://www.google.com/search?q=learn+{skill.replace(" ", "+")}',
                    'estimated_hours': 20
                })
        
        # Process preferred skills (medium priority)
        for skill in missing_preferred:
            courses = self._find_courses(skill)
            if courses:
                course = courses[0]
                recommendations.append({
                    'skill': skill,
                    'type': 'preferred',
                    'priority': 'medium',
                    'course_title': course['title'],
                    'provider': course['provider'],
                    'duration': course['duration'],
                    'level': course['level'],
                    'url': course.get('url', ''),
                    'estimated_hours': self._parse_duration(course['duration'])
                })
        
        return recommendations
    
    def _find_courses(self, skill):
        """Find courses for a specific skill"""
        # Direct match
        if skill in self.courses_db:
            return self.courses_db[skill]
        
        # Case-insensitive match
        for key in self.courses_db:
            if key.lower() == skill.lower():
                return self.courses_db[key]
        
        # Partial match
        for key in self.courses_db:
            if skill.lower() in key.lower() or key.lower() in skill.lower():
                return self.courses_db[key]
        
        return []
    
    def _parse_duration(self, duration_str):
        """Parse duration string to hours"""
        duration_str = duration_str.lower()
        
        # Extract hours
        if 'hour' in duration_str:
            import re
            match = re.search(r'(\d+)\s*hour', duration_str)
            if match:
                return int(match.group(1))
        
        # Convert weeks to hours (assuming 10 hours/week)
        if 'week' in duration_str:
            import re
            match = re.search(r'(\d+)\s*week', duration_str)
            if match:
                return int(match.group(1)) * 10
        
        # Convert months to hours (assuming 40 hours/month)
        if 'month' in duration_str:
            import re
            match = re.search(r'(\d+)\s*month', duration_str)
            if match:
                return int(match.group(1)) * 40
        
        # Default
        return 20
    
    def _calculate_match_percentage(self, matched, total):
        """Calculate match percentage"""
        if total == 0:
            return 100.0
        return round((matched / total) * 100, 1)
    
    def _estimate_weeks(self, total_hours):
        """Estimate weeks needed (assuming 10 hours/week study)"""
        if total_hours == 0:
            return 0
        return round(total_hours / 10, 1)
    
    def _calculate_readiness(self, matched_req, total_req, matched_pref, total_pref):
        """Calculate overall readiness score"""
        if total_req == 0:
            req_score = 100
        else:
            req_score = (matched_req / total_req) * 70  # 70% weight
        
        if total_pref == 0:
            pref_score = 30
        else:
            pref_score = (matched_pref / total_pref) * 30  # 30% weight
        
        return round(req_score + pref_score, 1)


# Test Skill Gap Analyzer
if __name__ == "__main__":
    analyzer = SkillGapAnalyzer()
    
    # Test case
    candidate_skills = {'Python', 'Django', 'SQL', 'Git'}
    required_skills = {'Python', 'Django', 'Docker', 'Kubernetes', 'AWS'}
    preferred_skills = {'React', 'MongoDB'}
    
    result = analyzer.analyze_gap(candidate_skills, required_skills, preferred_skills)
    
    print("Skill Gap Analysis Results:")
    print("=" * 60)
    print(f"\nMatched Required Skills: {', '.join(result['matched_required_skills'])}")
    print(f"Matched Preferred Skills: {', '.join(result['matched_preferred_skills'])}")
    print(f"\nMissing Required Skills: {', '.join(result['missing_required_skills'])}")
    print(f"Missing Preferred Skills: {', '.join(result['missing_preferred_skills'])}")
    print(f"\nMatch Percentage: {result['match_percentage']}%")
    print(f"Readiness Score: {result['readiness_score']}/100")
    print(f"\nTotal Learning Time: {result['total_learning_hours']} hours")
    print(f"Estimated Duration: {result['estimated_weeks']} weeks")
    
    print(f"\nRecommended Courses ({len(result['recommendations'])} total):")
    print("-" * 60)
    
    for i, rec in enumerate(result['recommendations'], 1):
        priority_mark = "[HIGH]" if rec['priority'] == 'high' else "[MED]" if rec['priority'] == 'medium' else "[LOW]"
        print(f"\n{i}. {priority_mark} {rec['skill']} ({rec['type'].upper()})")
        print(f"   Course: {rec['course_title']}")
        print(f"   Provider: {rec['provider']}")
        print(f"   Duration: {rec['duration']}")
        print(f"   Level: {rec['level']}")
        print(f"   URL: {rec['url']}")
