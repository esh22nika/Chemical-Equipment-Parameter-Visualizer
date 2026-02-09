import React, { useEffect, useState } from 'react';
import { Chart as ChartJS, ArcElement, CategoryScale, LinearScale, BarElement, LineElement, PointElement, Title, Tooltip, Legend, RadialLinearScale } from 'chart.js';
import { Pie, Bar, Line, Radar } from 'react-chartjs-2';
import SummaryCard from './SummaryCard';
import './Dashboard.css';

ChartJS.register(ArcElement, CategoryScale, LinearScale, BarElement, LineElement, PointElement, Title, Tooltip, Legend, RadialLinearScale);

function Dashboard({ dataset }) {
  const [chartData, setChartData] = useState(null);
  const [stats, setStats] = useState(null);

  useEffect(() => {
    if (dataset) {
      prepareChartData();
      calculateAdvancedStats();
    }
  }, [dataset]);

  const calculateAdvancedStats = () => {
    const flowrates = dataset.data.map(d => d.Flowrate);
    const pressures = dataset.data.map(d => d.Pressure);
    const temperatures = dataset.data.map(d => d.Temperature);

    const calculateStats = (arr) => {
      const sorted = [...arr].sort((a, b) => a - b);
      const min = Math.min(...arr);
      const max = Math.max(...arr);
      const mean = arr.reduce((a, b) => a + b, 0) / arr.length;
      const variance = arr.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / arr.length;
      const stdDev = Math.sqrt(variance);
      
      return { min, max, mean, stdDev, range: max - min };
    };

    setStats({
      flowrate: calculateStats(flowrates),
      pressure: calculateStats(pressures),
      temperature: calculateStats(temperatures),
    });
  };

  const prepareChartData = () => {
    const types = Object.keys(dataset.equipment_type_distribution);
    const counts = Object.values(dataset.equipment_type_distribution);

    const colors = ['#0A6EBD', '#00D4AA', '#F59E0B', '#DC2626', '#8B5CF6', '#EC4899'];

    const pieData = {
      labels: types,
      datasets: [
        {
          data: counts,
          backgroundColor: colors,
          borderColor: '#FFFFFF',
          borderWidth: 2,
          hoverOffset: 8,
        },
      ],
    };

    const barData = {
      labels: ['Flowrate', 'Pressure', 'Temperature'],
      datasets: [
        {
          label: 'Average Values',
          data: [
            dataset.avg_flowrate,
            dataset.avg_pressure,
            dataset.avg_temperature,
          ],
          backgroundColor: ['#0A6EBD', '#00D4AA', '#F59E0B'],
          borderRadius: 8,
          borderSkipped: false,
        },
      ],
    };

    const lineLabels = dataset.data.slice(0, 15).map((item) => item['Equipment Name'].substring(0, 10));
    const lineData = {
      labels: lineLabels,
      datasets: [
        {
          label: 'Flowrate',
          data: dataset.data.slice(0, 15).map((item) => item.Flowrate),
          borderColor: '#0A6EBD',
          backgroundColor: 'rgba(10, 110, 189, 0.1)',
          tension: 0.4,
          fill: true,
          pointRadius: 4,
          pointHoverRadius: 6,
        },
        {
          label: 'Pressure',
          data: dataset.data.slice(0, 15).map((item) => item.Pressure),
          borderColor: '#00D4AA',
          backgroundColor: 'rgba(0, 212, 170, 0.1)',
          tension: 0.4,
          fill: true,
          pointRadius: 4,
          pointHoverRadius: 6,
        },
        {
          label: 'Temperature',
          data: dataset.data.slice(0, 15).map((item) => item.Temperature),
          borderColor: '#F59E0B',
          backgroundColor: 'rgba(245, 158, 11, 0.1)',
          tension: 0.4,
          fill: true,
          pointRadius: 4,
          pointHoverRadius: 6,
        },
      ],
    };

    // Radar chart for parameter comparison
    const radarData = {
      labels: ['Min', 'Max', 'Avg', 'Range', 'Std Dev'],
      datasets: types.map((type, index) => {
        const typeData = dataset.data.filter(d => d.Type === type);
        const flowrates = typeData.map(d => d.Flowrate);
        const min = Math.min(...flowrates);
        const max = Math.max(...flowrates);
        const avg = flowrates.reduce((a, b) => a + b, 0) / flowrates.length;
        const range = max - min;
        const variance = flowrates.reduce((sum, val) => sum + Math.pow(val - avg, 2), 0) / flowrates.length;
        const stdDev = Math.sqrt(variance);

        return {
          label: type,
          data: [
            min / 200 * 100,
            max / 200 * 100,
            avg / 200 * 100,
            range / 100 * 100,
            stdDev / 50 * 100,
          ],
          borderColor: colors[index % colors.length],
          backgroundColor: colors[index % colors.length] + '20',
          borderWidth: 2,
        };
      }),
    };

    setChartData({ pieData, barData, lineData, radarData });
  };

  if (!dataset) {
    return (
      <div className="dashboard-empty-state">
        <div className="empty-state-content">
          <div className="empty-state-icon">
            <svg width="120" height="120" viewBox="0 0 120 120" fill="none">
              <circle cx="60" cy="60" r="50" stroke="var(--border)" strokeWidth="2" strokeDasharray="4 4" />
              <path
                d="M60 30V60L75 75"
                stroke="var(--text-tertiary)"
                strokeWidth="3"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              <circle cx="60" cy="60" r="4" fill="var(--primary)" />
            </svg>
          </div>
          <h2>Welcome to ChemFlow Analytics</h2>
          <p>Upload equipment data to start analyzing parameters and generating insights</p>
          <button className="btn btn-primary" style={{ marginTop: '1.5rem' }}>
            Upload Your First Dataset
          </button>
        </div>
      </div>
    );
  }

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          usePointStyle: true,
          padding: 16,
          font: {
            size: 13,
            family: 'Instrument Sans',
          },
        },
      },
      tooltip: {
        backgroundColor: 'rgba(15, 20, 25, 0.95)',
        padding: 12,
        titleFont: {
          size: 14,
          family: 'Instrument Sans',
        },
        bodyFont: {
          size: 13,
          family: 'IBM Plex Mono',
        },
        borderColor: 'rgba(255, 255, 255, 0.1)',
        borderWidth: 1,
      },
    },
  };

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <div>
          <h1>Analytics Dashboard</h1>
          <p className="dashboard-subtitle">
            <span className="text-mono">{dataset.filename}</span>
            <span className="separator">•</span>
            <span>{new Date(dataset.upload_date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}</span>
          </p>
        </div>
        <div className="dashboard-actions">
          <button className="btn btn-secondary">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M14 6L8 2L2 6V13C2 13.5304 2.21071 14.0391 2.58579 14.4142C2.96086 14.7893 3.46957 15 4 15H12C12.5304 15 13.0391 14.7893 13.4142 14.4142C13.7893 14.0391 14 13.5304 14 13V6Z" stroke="currentColor" strokeWidth="1.5"/>
              <path d="M6 15V8H10V15" stroke="currentColor" strokeWidth="1.5"/>
            </svg>
            Export Data
          </button>
          <button className="btn btn-primary">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M14 10V12.6667C14 13.0203 13.8595 13.3594 13.6095 13.6095C13.3594 13.8595 13.0203 14 12.6667 14H3.33333C2.97971 14 2.64057 13.8595 2.39052 13.6095C2.14048 13.3594 2 13.0203 2 12.6667V10" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
              <path d="M4.66667 6.66667L8 10L11.3333 6.66667" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M8 10V2" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
            </svg>
            Generate Report
          </button>
        </div>
      </div>

      <div className="summary-grid">
        <SummaryCard
          title="Total Equipment"
          value={dataset.total_count}
          subtitle="Active units"
          trend="+12%"
          trendUp={true}
          color="primary"
        />
        <SummaryCard
          title="Avg Flowrate"
          value={dataset.avg_flowrate.toFixed(1)}
          subtitle="L/min"
          trend="+5.2%"
          trendUp={true}
          color="accent"
        />
        <SummaryCard
          title="Avg Pressure"
          value={dataset.avg_pressure.toFixed(1)}
          subtitle="bar"
          trend="-2.1%"
          trendUp={false}
          color="warning"
        />
        <SummaryCard
          title="Avg Temperature"
          value={dataset.avg_temperature.toFixed(1)}
          subtitle="°C"
          trend="+3.8%"
          trendUp={true}
          color="success"
        />
      </div>

      {chartData && (
        <div className="charts-container">
          <div className="chart-row">
            <div className="chart-card span-2">
              <div className="chart-header">
                <div>
                  <h3>Parameter Trends</h3>
                  <p className="chart-description">Multi-parameter analysis across equipment</p>
                </div>
                <div className="chart-legend-inline">
                  <span className="legend-item">
                    <span className="legend-dot" style={{ background: '#0A6EBD' }}></span>
                    Flowrate
                  </span>
                  <span className="legend-item">
                    <span className="legend-dot" style={{ background: '#00D4AA' }}></span>
                    Pressure
                  </span>
                  <span className="legend-item">
                    <span className="legend-dot" style={{ background: '#F59E0B' }}></span>
                    Temperature
                  </span>
                </div>
              </div>
              <div className="chart-body" style={{ height: '320px' }}>
                <Line data={chartData.lineData} options={chartOptions} />
              </div>
            </div>

            <div className="chart-card">
              <div className="chart-header">
                <div>
                  <h3>Equipment Distribution</h3>
                  <p className="chart-description">By type classification</p>
                </div>
              </div>
              <div className="chart-body" style={{ height: '320px' }}>
                <Pie data={chartData.pieData} options={chartOptions} />
              </div>
            </div>
          </div>

          <div className="chart-row">
            <div className="chart-card">
              <div className="chart-header">
                <div>
                  <h3>Average Parameters</h3>
                  <p className="chart-description">Comparative analysis</p>
                </div>
              </div>
              <div className="chart-body" style={{ height: '280px' }}>
                <Bar
                  data={chartData.barData}
                  options={{
                    ...chartOptions,
                    plugins: {
                      ...chartOptions.plugins,
                      legend: { display: false },
                    },
                  }}
                />
              </div>
            </div>

            <div className="chart-card">
              <div className="chart-header">
                <div>
                  <h3>Performance Metrics</h3>
                  <p className="chart-description">Statistical distribution</p>
                </div>
              </div>
              <div className="chart-body" style={{ height: '280px' }}>
                <Radar data={chartData.radarData} options={chartOptions} />
              </div>
            </div>
          </div>
        </div>
      )}

      {stats && (
        <div className="stats-table-container">
          <div className="stats-table-header">
            <h3>Statistical Overview</h3>
            <p className="chart-description">Detailed parameter analysis</p>
          </div>
          <div className="stats-table">
            <table>
              <thead>
                <tr>
                  <th>Parameter</th>
                  <th>Min</th>
                  <th>Max</th>
                  <th>Mean</th>
                  <th>Std Dev</th>
                  <th>Range</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td className="param-name">
                    <span className="param-dot" style={{ background: '#0A6EBD' }}></span>
                    Flowrate
                  </td>
                  <td className="text-mono">{stats.flowrate.min.toFixed(2)}</td>
                  <td className="text-mono">{stats.flowrate.max.toFixed(2)}</td>
                  <td className="text-mono">{stats.flowrate.mean.toFixed(2)}</td>
                  <td className="text-mono">{stats.flowrate.stdDev.toFixed(2)}</td>
                  <td className="text-mono">{stats.flowrate.range.toFixed(2)}</td>
                </tr>
                <tr>
                  <td className="param-name">
                    <span className="param-dot" style={{ background: '#00D4AA' }}></span>
                    Pressure
                  </td>
                  <td className="text-mono">{stats.pressure.min.toFixed(2)}</td>
                  <td className="text-mono">{stats.pressure.max.toFixed(2)}</td>
                  <td className="text-mono">{stats.pressure.mean.toFixed(2)}</td>
                  <td className="text-mono">{stats.pressure.stdDev.toFixed(2)}</td>
                  <td className="text-mono">{stats.pressure.range.toFixed(2)}</td>
                </tr>
                <tr>
                  <td className="param-name">
                    <span className="param-dot" style={{ background: '#F59E0B' }}></span>
                    Temperature
                  </td>
                  <td className="text-mono">{stats.temperature.min.toFixed(2)}</td>
                  <td className="text-mono">{stats.temperature.max.toFixed(2)}</td>
                  <td className="text-mono">{stats.temperature.mean.toFixed(2)}</td>
                  <td className="text-mono">{stats.temperature.stdDev.toFixed(2)}</td>
                  <td className="text-mono">{stats.temperature.range.toFixed(2)}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}

export default Dashboard;