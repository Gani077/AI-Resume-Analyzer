from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
from werkzeug.utils import secure_filename
import traceback

# Import our custom modules
from resume_parser import extract_resume_text
from skill_extractor import extract_skills, extract_jd_skills
from analyzer import calculate_match_score, find_missing_skills, generate_recommendations

app = Flask(__name__)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx'}

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    """Handle resume analysis request."""
    try:
        # Check if resume file was uploaded
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file uploaded'}), 400
        
        file = request.files['resume']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check if file type is allowed
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Please upload PDF or DOCX files only'}), 400
        
        # Get job description from form
        job_description = request.form.get('job_description', '').strip()
        if not job_description:
            return jsonify({'error': 'Job description is required'}), 400
        
        # Extract text from resume
        try:
            resume_text = extract_resume_text(file)
            if not resume_text:
                return jsonify({'error': 'Could not extract text from resume. Please ensure the file contains readable text.'}), 400
        except Exception as e:
            return jsonify({'error': f'Error processing resume file: {str(e)}'}), 400
        
        # Extract skills from resume
        try:
            resume_skills = extract_skills(resume_text)
        except Exception as e:
            return jsonify({'error': f'Error extracting skills: {str(e)}'}), 400
        
        # Extract skills from job description
        try:
            jd_skills = extract_jd_skills(job_description)
        except Exception as e:
            return jsonify({'error': f'Error extracting job description skills: {str(e)}'}), 400
        
        # Find missing skills
        try:
            missing_skills = find_missing_skills(resume_skills, jd_skills)
        except Exception as e:
            return jsonify({'error': f'Error finding missing skills: {str(e)}'}), 400
        
        # Calculate match score
        try:
            score = calculate_match_score(resume_text, job_description)
        except Exception as e:
            return jsonify({'error': f'Error calculating match score: {str(e)}'}), 400
        
        # Generate recommendations
        try:
            recommendations = generate_recommendations(missing_skills)
        except Exception as e:
            return jsonify({'error': f'Error generating recommendations: {str(e)}'}), 400
        
        # Prepare response
        response_data = {
            'success': True,
            'match_score': score,
            'detected_skills': resume_skills,
            'missing_skills': missing_skills,
            'recommendations': recommendations,
            'resume_text_length': len(resume_text),
            'job_description_length': len(job_description)
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        # Log the full traceback for debugging
        app.logger.error(f"Error in analyze_resume: {str(e)}\n{traceback.format_exc()}")
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring."""
    return jsonify({'status': 'healthy', 'message': 'Resume Analyzer API is running'})

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error."""
    return jsonify({'error': 'File too large. Maximum file size is 16MB.'}), 413

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error occurred'}), 500

# Development server configuration
if __name__ == '__main__':
    # Check if required modules are available
    try:
        # Test imports
        from resume_parser import extract_resume_text
        from skill_extractor import extract_skills
        from analyzer import calculate_match_score
        print("✓ All modules imported successfully")
        
        # Test basic functionality
        test_text = "Python Java Machine Learning"
        test_skills = extract_skills(test_text)
        print(f"✓ Skill extraction working: {test_skills}")
        
        test_score = calculate_match_score("Python developer", "Looking for Python developer")
        print(f"✓ Match calculation working: {test_score}%")
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        print("Please ensure all required modules are installed:")
        print("pip install -r requirements.txt")
    except Exception as e:
        print(f"✗ Module test error: {e}")
    
    print("\nStarting Flask server...")
    print("Open http://127.0.0.1:5000 in your browser")
    
    app.run(debug=True, host='0.0.0.0', port=5000)