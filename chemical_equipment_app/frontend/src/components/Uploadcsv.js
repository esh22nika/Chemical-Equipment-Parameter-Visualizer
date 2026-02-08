import React, { useState } from 'react';
import { datasetService } from '../services/api';
import './UploadCSV.css';

function UploadCSV({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    setError('');
    setSuccess('');
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a CSV file');
      return;
    }

    if (!file.name.endsWith('.csv')) {
      setError('Please upload a CSV file');
      return;
    }

    setUploading(true);
    setError('');
    setSuccess('');

    try {
      const data = await datasetService.uploadCSV(file);
      setSuccess(`File "${file.name}" uploaded successfully!`);
      setTimeout(() => {
        onUploadSuccess(data);
      }, 1500);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to upload file');
    } finally {
      setUploading(false);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && droppedFile.name.endsWith('.csv')) {
      setFile(droppedFile);
      setError('');
      setSuccess('');
    } else {
      setError('Please drop a CSV file');
    }
  };

  return (
    <div className="upload-container">
      <h1>Upload CSV File</h1>
      <p className="upload-subtitle">
        Upload a CSV file with columns: Equipment Name, Type, Flowrate, Pressure, Temperature
      </p>

      <div
        className="upload-dropzone"
        onDragOver={handleDragOver}
        onDrop={handleDrop}
      >
        <div className="upload-icon">📁</div>
        <p>Drag and drop your CSV file here</p>
        <p className="upload-or">or</p>
        <label htmlFor="file-input" className="file-input-label">
          Browse Files
        </label>
        <input
          type="file"
          id="file-input"
          accept=".csv"
          onChange={handleFileChange}
          style={{ display: 'none' }}
        />
      </div>

      {file && (
        <div className="file-info">
          <p>Selected file: <strong>{file.name}</strong></p>
          <p>Size: {(file.size / 1024).toFixed(2)} KB</p>
        </div>
      )}

      {error && <div className="error-message">{error}</div>}
      {success && <div className="success-message">{success}</div>}

      <button
        onClick={handleUpload}
        disabled={!file || uploading}
        className="upload-button"
      >
        {uploading ? 'Uploading...' : 'Upload and Analyze'}
      </button>

      <div className="upload-instructions">
        <h3>CSV Format Requirements:</h3>
        <ul>
          <li>Column 1: Equipment Name (text)</li>
          <li>Column 2: Type (text)</li>
          <li>Column 3: Flowrate (number)</li>
          <li>Column 4: Pressure (number)</li>
          <li>Column 5: Temperature (number)</li>
        </ul>
      </div>
    </div>
  );
}

export default UploadCSV;