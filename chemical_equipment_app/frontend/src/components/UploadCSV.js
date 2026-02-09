import React, { useState } from 'react';
import { datasetService } from '../services/api';
import './UploadCSV.css';

function UploadCSV({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [dragActive, setDragActive] = useState(false);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      validateAndSetFile(selectedFile);
    }
  };

  const validateAndSetFile = (selectedFile) => {
    if (!selectedFile.name.endsWith('.csv')) {
      setError('Please upload a CSV file');
      setFile(null);
      return;
    }
    setFile(selectedFile);
    setError('');
    setSuccess('');
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a CSV file');
      return;
    }

    setUploading(true);
    setError('');
    setSuccess('');

    try {
      const data = await datasetService.uploadCSV(file);
      setSuccess(`Successfully uploaded "${file.name}"`);
      setTimeout(() => {
        onUploadSuccess(data);
      }, 1000);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to upload file');
    } finally {
      setUploading(false);
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) {
      validateAndSetFile(droppedFile);
    }
  };

  return (
    <div className="upload-container">
      <div className="upload-header">
        <h1>Upload Equipment Data</h1>
        <p className="upload-subtitle">
          Import CSV files containing chemical equipment parameters for analysis
        </p>
      </div>

      <div
        className={`upload-dropzone ${dragActive ? 'drag-active' : ''} ${file ? 'has-file' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        {!file ? (
          <>
            <div className="upload-icon">
              <svg width="64" height="64" viewBox="0 0 64 64" fill="none">
                <rect x="8" y="16" width="48" height="40" rx="4" stroke="currentColor" strokeWidth="2" strokeDasharray="4 4"/>
                <path d="M32 28V44M32 28L26 34M32 28L38 34" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"/>
                <circle cx="32" cy="44" r="2" fill="currentColor"/>
              </svg>
            </div>
            <h3>Drop your CSV file here</h3>
            <p>or click to browse from your computer</p>
            <input
              type="file"
              id="file-input"
              accept=".csv"
              onChange={handleFileChange}
              style={{ display: 'none' }}
            />
            <label htmlFor="file-input" className="btn btn-primary btn-upload">
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                <path d="M14 10V12.6667C14 13.0203 13.8595 13.3594 13.6095 13.6095C13.3594 13.8595 13.0203 14 12.6667 14H3.33333C2.97971 14 2.64057 13.8595 2.39052 13.6095C2.14048 13.3594 2 13.0203 2 12.6667V10" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                <path d="M8 2V10M8 2L5.33333 4.66667M8 2L10.6667 4.66667" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
              Choose File
            </label>
            <p className="helper-text">
              CSV with columns: Equipment Name, Type, Flowrate, Pressure, Temperature
            </p>
          </>
        ) : (
          <div className="file-preview">
            <div className="file-preview-icon">
              <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
                <path d="M28 4H12C11.2044 4 10.4413 4.31607 9.87868 4.87868C9.31607 5.44129 9 6.20435 9 7V41C9 41.7956 9.31607 42.5587 9.87868 43.1213C10.4413 43.6839 11.2044 44 12 44H36C36.7956 44 37.5587 43.6839 38.1213 43.1213C38.6839 42.5587 39 41.7956 39 41V15L28 4Z" stroke="var(--primary)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M28 4V15H39" stroke="var(--primary)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M24 36V24M20 28L24 24L28 28" stroke="var(--primary)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </div>
            <div className="file-preview-details">
              <h4>{file.name}</h4>
              <p className="text-mono">{(file.size / 1024).toFixed(2)} KB</p>
            </div>
            <button
              className="file-remove-btn"
              onClick={(e) => {
                e.stopPropagation();
                setFile(null);
              }}
            >
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                <path d="M12 4L4 12M4 4L12 12" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
              </svg>
            </button>
          </div>
        )}
      </div>

      {error && (
        <div className="alert alert-error">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <circle cx="8" cy="8" r="7" stroke="currentColor" strokeWidth="1.5"/>
            <path d="M8 4V8M8 10V12" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
          </svg>
          {error}
        </div>
      )}

      {success && (
        <div className="alert alert-success">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <circle cx="8" cy="8" r="7" stroke="currentColor" strokeWidth="1.5"/>
            <path d="M5 8L7 10L11 6" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
          {success}
        </div>
      )}

      <button
        onClick={handleUpload}
        disabled={!file || uploading}
        className="btn btn-primary btn-upload-action"
      >
        {uploading ? (
          <>
            <div className="btn-spinner"></div>
            Processing...
          </>
        ) : (
          <>
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M8 2L8 14M8 2L4 6M8 2L12 6" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
            Upload and Analyze
          </>
        )}
      </button>
    </div>
  );
}

export default UploadCSV;