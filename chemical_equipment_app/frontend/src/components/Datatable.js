import React from 'react';
import './DataTable.css';

function DataTable({ dataset }) {
  if (!dataset || !dataset.data) {
    return (
      <div className="data-table-empty">
        <h2>No Data Available</h2>
        <p>Please upload a CSV file first.</p>
      </div>
    );
  }

  return (
    <div className="data-table-container">
      <h1>Equipment Data</h1>
      <p className="data-table-subtitle">
        Showing {dataset.total_count} equipment records from {dataset.filename}
      </p>

      <div className="table-wrapper">
        <table className="data-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Equipment Name</th>
              <th>Type</th>
              <th>Flowrate</th>
              <th>Pressure</th>
              <th>Temperature</th>
            </tr>
          </thead>
          <tbody>
            {dataset.data.map((row, index) => (
              <tr key={index}>
                <td>{index + 1}</td>
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
  );
}

export default DataTable;