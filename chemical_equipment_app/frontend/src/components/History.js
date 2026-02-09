import React, { useState, useEffect } from 'react';
import { datasetService } from '../services/api';
import './History.css';

function History({ onSelectDataset }) {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const data = await datasetService.getHistory();
      setHistory(data);
    } catch (err) {
      setError('Failed to load history');
    } finally {
      setLoading(false);
    }
  };

  const handleSelect = async (datasetId) => {
    try {
      const data = await datasetService.getDataset(datasetId);
      onSelectDataset(data);
      window.dispatchEvent(new CustomEvent('changeView', { detail: 'dashboard' }));
    } catch (err) {
      setError('Failed to load dataset');
    }
  };

  const handleDelete = async (datasetId) => {
    if (window.confirm('Are you sure you want to delete this dataset?')) {
      try {
        await datasetService.deleteDataset(datasetId);
        fetchHistory();
      } catch (err) {
        setError('Failed to delete dataset');
      }
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    }).format(date);
  };

  if (loading) {
    return (
      <div className="history-loading">
        <div className="loading-spinner"></div>
        <p>Loading history...</p>
      </div>
    );
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  if (history.length === 0) {
    return (
      <div className="history-empty">
        <svg width="120" height="120" viewBox="0 0 120 120" fill="none">
          <circle cx="60" cy="60" r="50" stroke="#cbd5e1" strokeWidth="2"/>
          <path d="M60 35v25l15 15" stroke="#0ea5e9" strokeWidth="3" strokeLinecap="round"/>
        </svg>
        <h2>No Upload History</h2>
        <p>Your uploaded datasets will appear here.</p>
      </div>
    );
  }

  return (
    <div className="history-container">
      <div className="history-header">
        <div>
          <h1>Upload History</h1>
          <p className="subtitle">Last 5 uploaded datasets</p>
        </div>
        <button onClick={fetchHistory} className="refresh-button">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path d="M13.65 2.35A7.95 7.95 0 0 0 8 0C3.58 0 0 3.58 0 8s3.58 8 8 8c3.73 0 6.84-2.55 7.73-6h-2.08A5.99 5.99 0 0 1 8 14c-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L9 7h7V0l-2.35 2.35z" fill="currentColor"/>
          </svg>
          Refresh
        </button>
      </div>

      <div className="history-grid">
        {history.map((dataset, index) => (
          <div key={dataset.id} className="history-card" style={{ animationDelay: `${index * 0.1}s` }}>
            <div className="card-header">
              <div className="file-icon">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                  <path d="M4 4C4 3.44772 4.44772 3 5 3H9L11 5H15C15.5523 5 16 5.44772 16 6V15C16 15.5523 15.5523 16 15 16H5C4.44772 16 4 15.5523 4 15V4Z" stroke="currentColor" strokeWidth="1.5"/>
                </svg>
              </div>
              <div className="card-title">
                <h3>{dataset.filename}</h3>
                <span className="upload-date">{formatDate(dataset.upload_date)}</span>
              </div>
              <span className="dataset-badge">Dataset #{dataset.id}</span>
            </div>

            <div className="stats-grid">
              <div className="stat-item">
                <span className="stat-icon" style={{ backgroundColor: '#e0f2fe', color: '#0ea5e9' }}>
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                    <path d="M7 1L5 5M11 1L13 5M5 5H13M5 5L3 15H13L11 5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                  </svg>
                </span>
                <div className="stat-content">
                  <span className="stat-label">Count</span>
                  <span className="stat-value">{dataset.total_count}</span>
                </div>
              </div>

              <div className="stat-item">
                <span className="stat-icon" style={{ backgroundColor: '#d1fae5', color: '#06b6d4' }}>
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                    <path d="M8 14c3.31 0 6-2.69 6-6s-2.69-6-6-6-6 2.69-6 6 2.69 6 6 6z" stroke="currentColor" strokeWidth="1.5"/>
                  </svg>
                </span>
                <div className="stat-content">
                  <span className="stat-label">Flowrate</span>
                  <span className="stat-value">{dataset.avg_flowrate.toFixed(1)} L/min</span>
                </div>
              </div>

              <div className="stat-item">
                <span className="stat-icon" style={{ backgroundColor: '#fef3c7', color: '#f59e0b' }}>
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                    <circle cx="8" cy="8" r="6" stroke="currentColor" strokeWidth="1.5"/>
                  </svg>
                </span>
                <div className="stat-content">
                  <span className="stat-label">Pressure</span>
                  <span className="stat-value">{dataset.avg_pressure.toFixed(1)} bar</span>
                </div>
              </div>

              <div className="stat-item">
                <span className="stat-icon" style={{ backgroundColor: '#fee2e2', color: '#ef4444' }}>
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                    <path d="M10 10V2.5a2 2 0 0 0-4 0V10a3.5 3.5 0 1 0 4 0z" stroke="currentColor" strokeWidth="1.5"/>
                  </svg>
                </span>
                <div className="stat-content">
                  <span className="stat-label">Temp</span>
                  <span className="stat-value">{dataset.avg_temperature.toFixed(1)} °C</span>
                </div>
              </div>
            </div>

            <div className="equipment-types">
              <span className="types-label">Equipment Types:</span>
              <div className="type-badges">
                {Object.entries(dataset.equipment_type_distribution).map(([type, count]) => (
                  <span key={type} className="type-badge">
                    {type}: {count}
                  </span>
                ))}
              </div>
            </div>

            <div className="card-actions">
              <button onClick={() => handleSelect(dataset.id)} className="btn-view">
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                  <path d="M8 3C4.5 3 1.73 5.11 1 8c.73 2.89 3.5 5 7 5s6.27-2.11 7-5c-.73-2.89-3.5-5-7-5z" stroke="currentColor" strokeWidth="1.5"/>
                  <circle cx="8" cy="8" r="2" stroke="currentColor" strokeWidth="1.5"/>
                </svg>
                View Details
              </button>
              <button onClick={() => handleDelete(dataset.id)} className="btn-delete">
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                  <path d="M2 4h12M5.5 4V2.5A1.5 1.5 0 0 1 7 1h2a1.5 1.5 0 0 1 1.5 1.5V4m2 0v9.5A1.5 1.5 0 0 1 11 15H5a1.5 1.5 0 0 1-1.5-1.5V4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                </svg>
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default History;