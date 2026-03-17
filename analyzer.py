from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import string
from typing import Tuple, Dict

def preprocess_text(text: str) -> str:
    """
    Preprocess text by removing punctuation, converting to lowercase, and normalizing whitespace.
    
    Args:
        text (str): Input text to preprocess
        
    Returns:
        str: Preprocessed text
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Remove extra whitespace and newlines
    text = re.sub(r'\s+', ' ', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text

def calculate_match_score(resume_text: str, job_description: str) -> float:
    """
    Calculate similarity score between resume text and job description using TF-IDF and cosine similarity.
    
    Args:
        resume_text (str): Resume text to analyze
        job_description (str): Job description to compare against
        
    Returns:
        float: Match percentage (0-100)
    """
    if not resume_text or not job_description:
        return 0.0
    
    try:
        documents = [resume_text, job_description]
        
        vectorizer = TfidfVectorizer(stop_words="english")
        
        tfidf_matrix = vectorizer.fit_transform(documents)
        
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        
        score = similarity[0][0] * 100
        
        return round(score, 2)
        
    except Exception as e:
        print(f"Error calculating match score: {str(e)}")
        return 0.0

def get_detailed_analysis(resume_text: str, job_description: str) -> Dict:
    """
    Get detailed analysis including match score, common keywords, and recommendations.
    
    Args:
        resume_text (str): Resume text to analyze
        job_description (str): Job description to compare against
        
    Returns:
        Dict: Detailed analysis results
    """
    match_score = calculate_match_score(resume_text, job_description)
    
    # Extract keywords from both texts
    resume_keywords = extract_keywords(resume_text)
    job_keywords = extract_keywords(job_description)
    
    # Find common keywords
    common_keywords = list(set(resume_keywords) & set(job_keywords))
    
    # Find missing keywords (in job but not in resume)
    missing_keywords = list(set(job_keywords) - set(resume_keywords))
    
    # Generate recommendations based on match score
    recommendations = generate_recommendations(match_score, missing_keywords)
    
    return {
        'match_score': match_score,
        'resume_keywords': resume_keywords[:20],  # Top 20 keywords
        'job_keywords': job_keywords[:20],  # Top 20 keywords
        'common_keywords': common_keywords[:15],  # Top 15 common keywords
        'missing_keywords': missing_keywords[:15],  # Top 15 missing keywords
        'recommendations': recommendations
    }

def extract_keywords(text: str, top_n: int = 50) -> list:
    """
    Extract top keywords from text using TF-IDF.
    
    Args:
        text (str): Text to extract keywords from
        top_n (int): Number of top keywords to return
        
    Returns:
        list: List of top keywords
    """
    if not text:
        return []
    
    processed_text = preprocess_text(text)
    
    try:
        vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.8
        )
        
        tfidf_matrix = vectorizer.fit_transform([processed_text])
        feature_names = vectorizer.get_feature_names_out()
        tfidf_scores = tfidf_matrix.toarray()[0]
        
        # Get top keywords by TF-IDF score
        keyword_scores = list(zip(feature_names, tfidf_scores))
        keyword_scores.sort(key=lambda x: x[1], reverse=True)
        
        return [keyword for keyword, score in keyword_scores[:top_n] if score > 0]
        
    except Exception as e:
        print(f"Error extracting keywords: {str(e)}")
        return []

def find_missing_skills(resume_skills, jd_skills):
    """
    Find skills that are in job description but not in resume.
    
    Args:
        resume_skills (list): Skills extracted from resume
        jd_skills (list): Skills extracted from job description
        
    Returns:
        list: List of missing skills
    """
    missing = []
    
    resume_lower = [s.lower() for s in resume_skills]
    
    for skill in jd_skills:
        if skill.lower() not in resume_lower:
            missing.append(skill)
    
    return missing

def generate_recommendations(missing_skills):
    """
    Generate recommendations based on missing skills.
    
    Args:
        missing_skills (list): Skills missing from resume
        
    Returns:
        list: List of recommendations
    """
    if not missing_skills:
        return ["Your resume already matches most required skills."]
    
    recommendations = []
    
    for skill in missing_skills[:5]:
        recommendations.append(f"Consider adding experience or projects related to {skill}")
    
    return recommendations

def batch_compare(resumes: list, job_description: str) -> list:
    """
    Compare multiple resumes against a single job description.
    
    Args:
        resumes (list): List of resume texts
        job_description (str): Job description to compare against
        
    Returns:
        list: List of tuples (resume_index, match_score)
    """
    results = []
    
    for i, resume in enumerate(resumes):
        score = calculate_match_score(resume, job_description)
        results.append((i, score))
    
    # Sort by match score (descending)
    results.sort(key=lambda x: x[1], reverse=True)
    
    return results

# Example usage and testing
if __name__ == "__main__":
    # Sample resume and job description for testing
    sample_resume = """
    Experienced software developer with 5 years of experience in Python, Java, and JavaScript.
    Proficient in machine learning frameworks like TensorFlow and PyTorch.
    Strong background in web development using React, HTML, and CSS.
    Experience with SQL databases and cloud platforms like AWS.
    """
    
    sample_job_description = """
    We are looking for a Senior Software Developer with experience in Python and Java.
    The ideal candidate should have experience with machine learning, TensorFlow, and React.
    Knowledge of SQL databases and cloud platforms is required.
    Experience with DevOps tools like Docker is a plus.
    """
    
    # Calculate match score
    score = calculate_match_score(sample_resume, sample_job_description)
    print(f"Match Score: {score}%")
    
    # Get detailed analysis
    analysis = get_detailed_analysis(sample_resume, sample_job_description)
    print("\nDetailed Analysis:")
    print(f"Common Keywords: {analysis['common_keywords']}")
    print(f"Missing Keywords: {analysis['missing_keywords']}")
    print(f"Recommendations: {analysis['recommendations']}")