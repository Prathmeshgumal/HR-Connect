# Resume Upload System

A modern resume upload system with React frontend and Flask API backend, featuring optimized upload performance and drag-and-drop functionality.

## 🚀 Features

- **Modern React Frontend** with drag-and-drop file upload
- **Optimized Upload Performance** with compression and retry logic
- **Real-time Notifications** with toast messages
- **Responsive Design** with beautiful UI
- **File Validation** (PDF, DOC, DOCX up to 5MB)
- **Supabase Integration** for storage and database
- **API Backend** with CORS support

## 📁 Project Structure

```
epic_hr_basic_upload/
├── app.py                 # Flask API backend
├── optimized_upload.py    # Upload optimization module
├── requirements.txt       # Python dependencies
├── frontend/             # React frontend
│   ├── package.json
│   ├── public/
│   │   └── index.html
│   └── src/
│       ├── App.js
│       ├── index.js
│       ├── index.css
│       └── components/
│           ├── UploadForm.js
│           └── SubmissionsList.js
└── README.md
```

## 🛠️ Setup Instructions

### Prerequisites

- **Node.js** (v14 or higher)
- **Python** (v3.8 or higher)
- **npm** or **yarn**

### Backend Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   Create a `.env` file in the root directory:
   ```env
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   FLASK_SECRET_KEY=your_secret_key
   ```

3. **Run the Flask backend:**
   ```bash
   python app.py
   ```
   The API will run on `http://localhost:5000`

### Frontend Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install React dependencies:**
   ```bash
   npm install
   ```

3. **Start the React development server:**
   ```bash
   npm start
   ```
   The React app will run on `http://localhost:3000`

## 🎯 API Endpoints

### Upload Resume
- **POST** `/api/upload`
- **Body:** `multipart/form-data`
- **Fields:** `name`, `mobile_number`, `resume`

### Get Submissions
- **GET** `/api/submissions`
- **Response:** List of all uploaded resumes

### Health Check
- **GET** `/api/health`
- **Response:** API status

## 🎨 Frontend Features

### Upload Form
- **Drag & Drop** file upload
- **File validation** (type and size)
- **Real-time feedback** with toast notifications
- **Form validation** with error messages
- **Loading states** during upload

### Submissions List
- **Grid layout** for submissions
- **Download** and **View** buttons
- **Refresh** functionality
- **Responsive design**

## 🚀 Deployment

### Backend Deployment (Render)

1. **Update `requirements.txt`:**
   ```
   Flask==2.3.3
   supabase==1.0.4
   python-dotenv==1.0.0
   Werkzeug==2.3.7
   gunicorn==21.2.0
   flask-cors==4.0.0
   ```

2. **Render Configuration:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`

3. **Environment Variables:**
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
   - `FLASK_SECRET_KEY`

### Frontend Deployment

1. **Build the React app:**
   ```bash
   cd frontend
   npm run build
   ```

2. **Deploy the `build` folder** to your hosting service (Netlify, Vercel, etc.)

3. **Update API URL** in production:
   - Change the proxy in `package.json` to your deployed API URL
   - Or use environment variables for API configuration

## 🔧 Configuration

### Environment Variables

**Backend (.env):**
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_service_role_key
FLASK_SECRET_KEY=your_secret_key
```

**Frontend (package.json):**
```json
{
  "proxy": "http://localhost:5000"
}
```

### File Upload Limits

- **Max file size:** 5MB
- **Allowed formats:** PDF, DOC, DOCX
- **Compression:** Automatic for files > 1MB

## 🐛 Troubleshooting

### Common Issues

1. **CORS Errors:**
   - Ensure `flask-cors` is installed
   - Check that CORS is enabled in `app.py`

2. **Upload Failures:**
   - Check Supabase credentials
   - Verify file size and type
   - Check network connectivity

3. **React Build Errors:**
   - Clear `node_modules` and reinstall
   - Check Node.js version compatibility

4. **API Connection Issues:**
   - Verify backend is running on port 5000
   - Check proxy configuration in `package.json`

### Development Tips

- **Backend:** Use `python app.py` for development
- **Frontend:** Use `npm start` for hot reloading
- **API Testing:** Use Postman or curl to test endpoints
- **Logs:** Check browser console and Flask logs for errors

## 📊 Performance Optimizations

- **File compression** for large uploads
- **Retry logic** with exponential backoff
- **Parallel processing** for chunked uploads
- **Memory optimization** (direct file reading)
- **Error handling** with graceful fallbacks

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

---

**Ready to deploy?** Follow the setup instructions above and you'll have a modern, optimized resume upload system running! 🚀 