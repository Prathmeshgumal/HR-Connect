from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from supabase import create_client, Client
import os
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from optimized_upload import optimize_upload_performance

app = Flask(__name__)
# Load environment variables
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY')

# Validate environment variables
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env file")

app.secret_key = FLASK_SECRET_KEY or 'fallback-secret-key'

# Initialize Supabase client
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    raise

# File upload configuration
UPLOAD_FOLDER = 'temp_uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
CHUNK_SIZE = 1024 * 1024  # 1MB chunks for faster uploads

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Thread pool for async operations
executor = ThreadPoolExecutor(max_workers=3)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_to_supabase_storage_optimized(file_data, storage_path, file_extension):
    """Advanced optimized upload with compression and retry logic"""
    try:
        # Use the advanced optimization module
        result = optimize_upload_performance(supabase, file_data, storage_path, file_extension)
        return result['result'] if result['success'] else None
    except Exception as e:
        # Fallback to basic upload
        return supabase.storage.from_('resumes').upload(
            storage_path, 
            file_data,
            file_options={"content-type": f"application/{file_extension}"}
        )

def save_to_database(user_data):
    """Save user data to database with optimized connection"""
    return supabase.table('user_resumes').insert(user_data).execute()

def get_public_url(storage_path):
    """Get public URL for uploaded file"""
    return supabase.storage.from_('resumes').get_public_url(storage_path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_resume():
    try:
        # Get form data
        name = request.form.get('name')
        mobile_number = request.form.get('mobile_number')
        
        # Validate required fields
        if not name or not mobile_number:
            flash('Name and mobile number are required!', 'error')
            return redirect(url_for('index'))
        
        # Check if file was uploaded
        if 'resume' not in request.files:
            flash('No resume file uploaded!', 'error')
            return redirect(url_for('index'))
        
        file = request.files['resume']
        
        if file.filename == '':
            flash('No file selected!', 'error')
            return redirect(url_for('index'))
        
        if file and allowed_file(file.filename):
            # Generate unique filename
            file_extension = file.filename.rsplit('.', 1)[1].lower()
            unique_filename = f"{uuid.uuid4()}.{file_extension}"
            storage_path = f"resumes/{unique_filename}"
            
            # Read file directly into memory (optimized)
            file_data = file.read()
            
            try:
                # Upload file to Supabase Storage (optimized)
                storage_response = upload_to_supabase_storage_optimized(file_data, storage_path, file_extension)
                
                if storage_response:
                    # Get public URL for the uploaded file
                    public_url = get_public_url(storage_path)
                    
                    # Insert user data into database
                    user_data = {
                        'name': name,
                        'mobile_number': mobile_number,
                        'resume_filename': file.filename,
                        'resume_path': storage_path,
                        'resume_url': public_url,
                        'created_at': datetime.now().isoformat()
                    }
                    
                    db_response = save_to_database(user_data)
                    
                    if db_response.data:
                        flash('Resume uploaded successfully!', 'success')
                    else:
                        flash('Error saving to database!', 'error')
                else:
                    flash('Error uploading file to storage!', 'error')
                
            except Exception as e:
                flash(f'Error processing upload: {str(e)}', 'error')
        
        else:
            flash('Invalid file type! Please upload PDF, DOC, or DOCX files only.', 'error')
    
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/submissions')
def view_submissions():
    try:
        response = supabase.table('user_resumes').select('*').order('created_at', desc=True).execute()
        submissions = response.data if response.data else []
        return render_template('submissions.html', submissions=submissions)
    except Exception as e:
        flash(f'Error fetching submissions: {str(e)}', 'error')
        return render_template('submissions.html', submissions=[])

if __name__ == '__main__':
    app.run(debug=True)