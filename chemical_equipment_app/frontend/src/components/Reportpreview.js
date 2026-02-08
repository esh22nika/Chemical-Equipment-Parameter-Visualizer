import React from 'react';
import { datasetService } from '../services/api';
import './ReportPreview.css';

function ReportPreview({ dataset }) {
  const handleDownloadPDF = async () => {
    if (!dataset) return;
    
    try {
      await datasetService.downloadPDF(dataset.id);
    } catch (err) {
      alert('Failed to download PDF');
    }
  };

  if (!dataset) {
    return (
      <div className="report-empty">
        <h2>No Dataset Selected</h2>
        <p>Please upload or select a dataset to generate a report.</p>
      </div>
    );
  }

  return (
    <div className="report-container">
      <h1>Report Preview</h1>
      <p className="report-subtitle">Generate PDF report for {dataset.filename}</p>

      <div className="report-preview">
        <div className="report-section">
          <h2>Dataset Information</h2>
          <div className="info-grid">
            <div className="info-item">
              <strong>Filename:</strong> {dataset.filename}
            </div>
            <div className="info-item">
              <strong>Upload Date:</strong>{' '}
              {new Date(dataset.upload_date).toLocaleString()}
            </div>
            <div className="info-item">
              <strong>Total Equipment:</strong> {dataset.total_count}
            </div>
          </div>
        </div>

        <div className="report-section">
          <h2>Summary Statistics</h2>
          <table className="summary-table">
            <thead>
              <tr>
                <th>Metric</th>
                <th>Value</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Average Flowrate</td>
                <td>{dataset.avg_flowrate.toFixed(2)}</td>
              </tr>
              <tr>
                <td>Average Pressure</td>
                <td>{dataset.avg_pressure.toFixed(2)}</td>
              </tr>
              <tr>
                <td>Average Temperature</td>
                <td>{dataset.avg_temperature.toFixed(2)}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div className="report-section">
          <h2>Equipment Type Distribution</h2>
          <table className="distribution-table">
            <thead>
              <tr>
                <th>Equipment Type</th>
                <th>Count</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(dataset.equipment_type_distribution).map(
                ([type, count]) => (
                  <tr key={type}>
                    <td>{type}</td>
                    <td>{count}</td>
                  </tr>
                )
              )}
            </tbody>
          </table>
        </div>

        <div className="report-section">
          <h2>Equipment Data Sample (First 10 Items)</h2>
          <div className="table-wrapper">
            <table className="data-preview-table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Type</th>
                  <th>Flowrate</th>
                  <th>Pressure</th>
                  <th>Temperature</th>
                </tr>
              </thead>
              <tbody>
                {dataset.data.slice(0, 10).map((row, index) => (
                  <tr key={index}>
                    <td>{row['Equipment Name']}</td>
                    <td>{row.Type}</td>
                    <td>{row.Flowrate.toFixed(2)}</td>
                    <td>{row.Pressure.toFixed(2)}</td>
                    <td>{row.Temperature.toFixed(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div className="report-actions">
        <button onClick={handleDownloadPDF} className="download-button">
          📄 Download PDF Report
        </button>
      </div>
    </div>
  );
}

export default ReportPreview;