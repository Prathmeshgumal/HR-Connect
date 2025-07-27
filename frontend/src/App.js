import React, { useState } from 'react';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import UploadForm from './components/UploadForm';
import SubmissionsList from './components/SubmissionsList';

function App() {
  const [currentPage, setCurrentPage] = useState('upload');

  return (
    <div className="App">
      <nav className="navbar">
        <div className="navbar-content">
          <a href="#" className="navbar-brand" onClick={() => setCurrentPage('upload')}>
            Resume Upload System
          </a>
          <div className="navbar-nav">
            <a 
              href="#" 
              className={`nav-link ${currentPage === 'upload' ? 'active' : ''}`}
              onClick={() => setCurrentPage('upload')}
            >
              Upload
            </a>
            <a 
              href="#" 
              className={`nav-link ${currentPage === 'submissions' ? 'active' : ''}`}
              onClick={() => setCurrentPage('submissions')}
            >
              View Submissions
            </a>
          </div>
        </div>
      </nav>

      <div className="container">
        {currentPage === 'upload' ? (
          <UploadForm />
        ) : (
          <SubmissionsList />
        )}
      </div>

      <ToastContainer
        position="top-right"
        autoClose={5000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
      />
    </div>
  );
}

export default App; 