import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import { toast } from 'react-toastify';

const UploadForm = () => {
  const [formData, setFormData] = useState({
    name: '',
    mobile_number: ''
  });
  const [uploadedFile, setUploadedFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);

  const onDrop = useCallback((acceptedFiles) => {
    const file = acceptedFiles[0];
    if (file) {
      // Check file type
      const allowedTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
      if (!allowedTypes.includes(file.type)) {
        toast.error('Please upload only PDF, DOC, or DOCX files!');
        return;
      }
      
      // Check file size (5MB limit)
      if (file.size > 5 * 1024 * 1024) {
        toast.error('File size must be less than 5MB!');
        return;
      }
      
      setUploadedFile(file);
      toast.success('File selected successfully!');
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/msword': ['.doc'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx']
    },
    multiple: false
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.name || !formData.mobile_number) {
      toast.error('Please fill in all required fields!');
      return;
    }
    
    if (!uploadedFile) {
      toast.error('Please select a file to upload!');
      return;
    }

    setIsUploading(true);

    try {
      const formDataToSend = new FormData();
      formDataToSend.append('name', formData.name);
      formDataToSend.append('mobile_number', formData.mobile_number);
      formDataToSend.append('resume', uploadedFile);

      const response = await axios.post('/api/upload', formDataToSend, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (response.data.success) {
        toast.success('Resume uploaded successfully!');
        // Reset form
        setFormData({ name: '', mobile_number: '' });
        setUploadedFile(null);
      } else {
        toast.error(response.data.error || 'Upload failed!');
      }
    } catch (error) {
      console.error('Upload error:', error);
      const errorMessage = error.response?.data?.error || 'Upload failed! Please try again.';
      toast.error(errorMessage);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="card">
      <h2 style={{ marginBottom: '2rem', color: '#333', textAlign: 'center' }}>
        Upload Your Resume
      </h2>
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="name" className="form-label">
            Full Name *
          </label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleInputChange}
            className="form-input"
            placeholder="Enter your full name"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="mobile_number" className="form-label">
            Mobile Number *
          </label>
          <input
            type="tel"
            id="mobile_number"
            name="mobile_number"
            value={formData.mobile_number}
            onChange={handleInputChange}
            className="form-input"
            placeholder="Enter 10-digit mobile number"
            pattern="[0-9]{10}"
            required
          />
          <small style={{ color: '#666', fontSize: '0.875rem' }}>
            Enter 10-digit mobile number
          </small>
        </div>

        <div className="form-group">
          <label className="form-label">Resume *</label>
          <div
            {...getRootProps()}
            className={`dropzone ${isDragActive ? 'drag-active' : ''}`}
          >
            <input {...getInputProps()} />
            {uploadedFile ? (
              <div>
                <p style={{ color: '#28a745', fontWeight: 'bold' }}>
                  ✓ File selected: {uploadedFile.name}
                </p>
                <p style={{ fontSize: '0.875rem', color: '#666' }}>
                  Size: {(uploadedFile.size / 1024 / 1024).toFixed(2)} MB
                </p>
              </div>
            ) : (
              <div>
                <p style={{ fontSize: '1.1rem', marginBottom: '0.5rem' }}>
                  {isDragActive
                    ? 'Drop the file here...'
                    : 'Drag & drop a file here, or click to select'}
                </p>
                <p style={{ fontSize: '0.875rem', color: '#666' }}>
                  Supported formats: PDF, DOC, DOCX (Max size: 5MB)
                </p>
              </div>
            )}
          </div>
        </div>

        <button
          type="submit"
          className="btn btn-primary"
          disabled={isUploading}
          style={{ width: '100%', marginTop: '1rem' }}
        >
          {isUploading ? 'Uploading...' : 'Upload Resume'}
        </button>
      </form>
    </div>
  );
};

export default UploadForm; 