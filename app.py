from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from supabase import create_client, Client
import os
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime

app = Flask(__name__)

# Load environment variables
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY')

# Debug: Print the loaded values (remove this after testing)
print(f"SUPABASE_URL: {SUPABASE_URL}")
print(f"SUPABASE_KEY: {SUPABASE_KEY[:20]}..." if SUPABASE_KEY else "SUPABASE_KEY: None")
print(f"FLASK_SECRET_KEY: {FLASK_SECRET_KEY}")

# Validate environment variables
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env file")

app.secret_key = FLASK_SECRET_KEY or 'fallback-secret-key'

# Initialize Supabase client
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("Supabase client initialized successfully!")
except Exception as e:
    print(f"Error initializing Supabase client: {e}")
    raise

# File upload configuration
UPLOAD_FOLDER = 'temp_uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
            
            # Save file temporarily
            temp_filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(temp_filepath)
            
            try:
                # Upload file to Supabase Storage
                with open(temp_filepath, 'rb') as f:
                    file_data = f.read()
                
                storage_path = f"resumes/{unique_filename}"
                
                # Upload to Supabase Storage
                storage_response = supabase.storage.from_('resumes').upload(
                    storage_path, 
                    file_data,
                    file_options={"content-type": f"application/{file_extension}"}
                )
                
                if storage_response:
                    # Get public URL for the uploaded file
                    public_url = supabase.storage.from_('resumes').get_public_url(storage_path)
                    
                    # Insert user data into database
                    user_data = {
                        'name': name,
                        'mobile_number': mobile_number,
                        'resume_filename': file.filename,
                        'resume_path': storage_path,
                        'resume_url': public_url,
                        'created_at': datetime.now().isoformat()
                    }
                    
                    db_response = supabase.table('user_resumes').insert(user_data).execute()
                    
                    if db_response.data:
                        flash('Resume uploaded successfully!', 'success')
                    else:
                        flash('Error saving to database!', 'error')
                else:
                    flash('Error uploading file to storage!', 'error')
                
            except Exception as e:
                flash(f'Error processing upload: {str(e)}', 'error')
            
            finally:
                # Clean up temporary file
                if os.path.exists(temp_filepath):
                    os.remove(temp_filepath)
        
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