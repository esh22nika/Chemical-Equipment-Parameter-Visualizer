import React, { useState } from 'react';
import { datasetService } from '../services/api';
import './ReportPreview.css';
import { jsPDF } from 'jspdf';
import html2canvas from 'html2canvas';


function ReportPreview({ dataset }) {
  const [downloading, setDownloading] = useState(false);
  const [error, setError] = useState('');

  const handleDownloadPDF = async () => {
  const element = document.getElementById('report-content');
  if (!element) {
    setError('Report content not found');
    return;
  }

  setDownloading(true);
  setError('');

  try {
    const canvas = await html2canvas(element, {
      scale: 2,
      useCORS: true
    });

    const imgData = canvas.toDataURL('image/png');

    const pdf = new jsPDF({
      orientation: 'p',
      unit: 'mm',
      format: 'a4'
    });

    const pdfWidth = pdf.internal.pageSize.getWidth();
    const pdfHeight = (canvas.height * pdfWidth) / canvas.width;

    pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
    pdf.save(`${dataset.filename}_Report.pdf`);
  } catch (err) {
    console.error('PDF generation error:', err);
    setError('Failed to generate PDF report.');
  } finally {
    setDownloading(false);
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

      {error && (
        <div className="alert alert-error" style={{ marginBottom: '1rem' }}>
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <circle cx="8" cy="8" r="7" stroke="currentColor" strokeWidth="1.5"/>
            <path d="M8 4V8M8 10V12" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
          </svg>
          {error}
        </div>
      )}

      <div className="report-preview" id="report-content">
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
                <td>{dataset.avg_flowrate.toFixed(2)} L/min</td>
              </tr>
              <tr>
                <td>Average Pressure</td>
                <td>{dataset.avg_pressure.toFixed(2)} bar</td>
              </tr>
              <tr>
                <td>Average Temperature</td>
                <td>{dataset.avg_temperature.toFixed(2)} °C</td>
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
              {Object.entries(dataset.equipment_type_distribution || {}).map(
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
                {(dataset.data || []).slice(0, 10).map((row, index) => (
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
        <button 
          onClick={handleDownloadPDF} 
          className="download-button"
          disabled={downloading}
        >
          {downloading ? (
            <>
              <div className="btn-spinner"></div>
              Generating PDF...
            </>
          ) : (
            <>
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                <path d="M14 10V12.6667C14 13.0203 13.8595 13.3594 13.6095 13.6095C13.3594 13.8595 13.0203 14 12.6667 14H3.33333C2.97971 14 2.64057 13.8595 2.39052 13.6095C2.14048 13.3594 2 13.0203 2 12.6667V10" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                <path d="M4.66667 6.66667L8 10L11.3333 6.66667" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M8 10V2" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
              </svg>
              Download PDF Report
            </>
          )}
        </button>
      </div>
    </div>
  );
}

export default ReportPreview;