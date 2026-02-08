import React, { useEffect, useState } from 'react';
import { Chart as ChartJS, ArcElement, CategoryScale, LinearScale, BarElement, LineElement, PointElement, Title, Tooltip, Legend } from 'chart.js';
import { Pie, Bar, Line } from 'react-chartjs-2';
import SummaryCard from './SummaryCard';
import './Dashboard.css';

ChartJS.register(ArcElement, CategoryScale, LinearScale, BarElement, LineElement, PointElement, Title, Tooltip, Legend);

function Dashboard({ dataset }) {
  const [chartData, setChartData] = useState(null);

  useEffect(() => {
    if (dataset) {
      prepareChartData();
    }
  }, [dataset]);

  const prepareChartData = () => {
    // Equipment Type Distribution (Pie Chart)
    const typeLabels = Object.keys(dataset.equipment_type_distribution);
    const typeCounts = Object.values(dataset.equipment_type_distribution);

    const pieData = {
      labels: typeLabels,
      datasets: [
        {
          data: typeCounts,
          backgroundColor: [
            '#3b82f6',
            '#10b981',
            '#f59e0b',
            '#ef4444',
            '#8b5cf6',
            '#ec4899',
            '#14b8a6',
          ],
        },
      ],
    };

    // Parameter Comparison (Bar Chart)
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
          backgroundColor: ['#3b82f6', '#10b981', '#f59e0b'],
        },
      ],
    };

    // Equipment Data (Line Chart - First 10 items)
    const lineLabels = dataset.data.slice(0, 10).map((item) => item['Equipment Name']);
    const lineData = {
      labels: lineLabels,
      datasets: [
        {
          label: 'Flowrate',
          data: dataset.data.slice(0, 10).map((item) => item.Flowrate),
          borderColor: '#3b82f6',
          backgroundColor: 'rgba(59, 130, 246, 0.1)',
        },
        {
          label: 'Pressure',
          data: dataset.data.slice(0, 10).map((item) => item.Pressure),
          borderColor: '#10b981',
          backgroundColor: 'rgba(16, 185, 129, 0.1)',
        },
        {
          label: 'Temperature',
          data: dataset.data.slice(0, 10).map((item) => item.Temperature),
          borderColor: '#f59e0b',
          backgroundColor: 'rgba(245, 158, 11, 0.1)',
        },
      ],
    };

    setChartData({ pieData, barData, lineData });
  };

  if (!dataset) {
    return (
      <div className="dashboard-empty">
        <h2>Welcome to Chemical Equipment Analyzer</h2>
        <p>Upload a CSV file to get started with analysis and visualization.</p>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <h1>Dashboard</h1>
      <p className="dashboard-subtitle">Dataset: {dataset.filename}</p>

      <div className="summary-cards">
        <SummaryCard
          title="Total Equipment"
          value={dataset.total_count}
          icon="📊"
        />
        <SummaryCard
          title="Avg Flowrate"
          value={dataset.avg_flowrate.toFixed(2)}
          icon="💧"
        />
        <SummaryCard
          title="Avg Pressure"
          value={dataset.avg_pressure.toFixed(2)}
          icon="⚡"
        />
        <SummaryCard
          title="Avg Temperature"
          value={dataset.avg_temperature.toFixed(2)}
          icon="🌡️"
        />
      </div>

      {chartData && (
        <div className="charts-grid">
          <div className="chart-container">
            <h3>Equipment Type Distribution</h3>
            <Pie data={chartData.pieData} />
          </div>

          <div className="chart-container">
            <h3>Average Parameters</h3>
            <Bar
              data={chartData.barData}
              options={{
                responsive: true,
                plugins: {
                  legend: {
                    display: false,
                  },
                },
              }}
            />
          </div>

          <div className="chart-container full-width">
            <h3>Equipment Parameters Trend (First 10 Items)</h3>
            <Line
              data={chartData.lineData}
              options={{
                responsive: true,
                plugins: {
                  legend: {
                    position: 'top',
                  },
                },
              }}
            />
          </div>
        </div>
      )}
    </div>
  );
}

export default Dashboard;