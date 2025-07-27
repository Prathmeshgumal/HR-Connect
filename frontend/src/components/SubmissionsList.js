import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { toast } from 'react-toastify';

const SubmissionsList = () => {
  const [submissions, setSubmissions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchSubmissions();
  }, []);

  const fetchSubmissions = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/submissions');
      
      if (response.data.success) {
        setSubmissions(response.data.data);
      } else {
        setError('Failed to fetch submissions');
        toast.error('Failed to fetch submissions');
      }
    } catch (error) {
      console.error('Error fetching submissions:', error);
      setError('Error fetching submissions');
      toast.error('Error fetching submissions');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    try {
      // Parse the ISO string and create a Date object
      const date = new Date(dateString);
      
      // Check if the date is valid
      if (isNaN(date.getTime())) {
        return 'Invalid date';
      }
      
      // Convert UTC to IST (UTC+5:30)
      // IST is UTC+5:30, so we add 5 hours and 30 minutes
      const istOffset = 5.5 * 60 * 60 * 1000; // 5.5 hours in milliseconds
      const istDate = new Date(date.getTime() + istOffset);
      
      // Format the date in IST
      const formattedDate = istDate.toLocaleDateString('en-IN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
      }) + ' IST';
      
      return formattedDate;
    } catch (error) {
      console.error('Error formatting date:', error);
      return 'Invalid date';
    }
  };

  const handleDownload = (url, filename) => {
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  if (loading) {
    return (
      <div className="card">
        <div className="loading">
          <h2>Loading submissions...</h2>
          <p>Please wait while we fetch the data.</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="card">
        <div className="error">
          <h2>Error</h2>
          <p>{error}</p>
          <button 
            className="btn btn-primary" 
            onClick={fetchSubmissions}
            style={{ marginTop: '1rem' }}
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h2 style={{ color: '#333' }}>Resume Submissions</h2>
        <button 
          className="btn btn-secondary" 
          onClick={fetchSubmissions}
        >
          Refresh
        </button>
      </div>

      {submissions.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '3rem', color: '#666' }}>
          <h3>No submissions yet</h3>
          <p>Upload resumes to see them here.</p>
        </div>
      ) : (
        <div className="submissions-grid">
          {submissions.map((submission, index) => (
            <div key={index} className="submission-card">
              <div style={{ marginBottom: '1rem' }}>
                <h3 style={{ color: '#333', marginBottom: '0.5rem' }}>
                  {submission.name}
                </h3>
                <p style={{ color: '#666', marginBottom: '0.5rem' }}>
                  📱 {submission.mobile_number}
                </p>
                <p style={{ color: '#666', fontSize: '0.875rem' }}>
                  📄 {submission.resume_filename}
                </p>
                <p style={{ color: '#666', fontSize: '0.875rem' }}>
                  📅 {formatDate(submission.created_at)}
                </p>
              </div>
              
              <div style={{ display: 'flex', gap: '0.5rem' }}>
                <button
                  className="btn btn-primary"
                  onClick={() => handleDownload(submission.resume_url, submission.resume_filename)}
                  style={{ flex: 1 }}
                >
                  Download
                </button>
                <a
                  href={submission.resume_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn btn-secondary"
                  style={{ flex: 1, textAlign: 'center' }}
                >
                  View
                </a>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default SubmissionsList; 