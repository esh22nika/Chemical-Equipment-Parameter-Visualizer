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

  if (loading) {
    return <div className="history-loading">Loading history...</div>;
  }

  if (error) {
    return <div className="history-error">{error}</div>;
  }

  if (history.length === 0) {
    return (
      <div className="history-empty">
        <h2>No Upload History</h2>
        <p>Your uploaded datasets will appear here.</p>
      </div>
    );
  }

  return (
    <div className="history-container">
      <h1>Upload History</h1>
      <p className="history-subtitle">Last 5 uploaded datasets</p>

      <div className="history-list">
        {history.map((dataset) => (
          <div key={dataset.id} className="history-card">
            <div className="history-header">
              <h3>{dataset.filename}</h3>
              <span className="history-date">
                {new Date(dataset.upload_date).toLocaleString()}
              </span>
            </div>

            <div className="history-stats">
              <div className="stat">
                <span className="stat-label">Total Count:</span>
                <span className="stat-value">{dataset.total_count}</span>
              </div>
              <div className="stat">
                <span className="stat-label">Avg Flowrate:</span>
                <span className="stat-value">{dataset.avg_flowrate.toFixed(2)}</span>
              </div>
              <div className="stat">
                <span className="stat-label">Avg Pressure:</span>
                <span className="stat-value">{dataset.avg_pressure.toFixed(2)}</span>
              </div>
              <div className="stat">
                <span className="stat-label">Avg Temperature:</span>
                <span className="stat-value">{dataset.avg_temperature.toFixed(2)}</span>
              </div>
            </div>

            <div className="equipment-types">
              <strong>Equipment Types:</strong>
              <div className="type-badges">
                {Object.entries(dataset.equipment_type_distribution).map(
                  ([type, count]) => (
                    <span key={type} className="type-badge">
                      {type}: {count}
                    </span>
                  )
                )}
              </div>
            </div>

            <div className="history-actions">
              <button
                onClick={() => handleSelect(dataset.id)}
                className="btn-view"
              >
                View Details
              </button>
              <button
                onClick={() => handleDelete(dataset.id)}
                className="btn-delete"
              >
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default History;