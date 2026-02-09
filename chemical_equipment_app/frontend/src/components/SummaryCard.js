import React from 'react';
import './SummaryCard.css';

function SummaryCard({ title, value, subtitle, trend, trendUp, color = 'primary' }) {
  const colorMap = {
    primary: '#0A6EBD',
    accent: '#00D4AA',
    warning: '#F59E0B',
    success: '#059669',
  };

  return (
    <div className="summary-card" data-color={color}>
      <div className="summary-card-header">
        <span className="summary-card-title">{title}</span>
        {trend && (
          <div className={`trend-badge ${trendUp ? 'trend-up' : 'trend-down'}`}>
            <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
              {trendUp ? (
                <path d="M6 9V3M6 3L3 6M6 3L9 6" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
              ) : (
                <path d="M6 3V9M6 9L3 6M6 9L9 6" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
              )}
            </svg>
            {trend}
          </div>
        )}
      </div>
      
      <div className="summary-card-body">
        <div className="summary-value-container">
          <span className="summary-value">{value}</span>
          <span className="summary-subtitle">{subtitle}</span>
        </div>
        
        <div className="summary-chart">
          <svg width="80" height="40" viewBox="0 0 80 40" fill="none">
            <path 
              d="M0 25 L10 20 L20 28 L30 15 L40 22 L50 18 L60 25 L70 12 L80 20" 
              stroke={colorMap[color]} 
              strokeWidth="2" 
              fill="none"
              strokeLinecap="round"
              strokeLinejoin="round"
              opacity="0.5"
            />
            <path 
              d="M0 25 L10 20 L20 28 L30 15 L40 22 L50 18 L60 25 L70 12 L80 20 L80 40 L0 40 Z" 
              fill={`url(#gradient-${color})`}
              opacity="0.2"
            />
            <defs>
              <linearGradient id={`gradient-${color}`} x1="0" y1="0" x2="0" y2="40">
                <stop offset="0%" stopColor={colorMap[color]} stopOpacity="0.4"/>
                <stop offset="100%" stopColor={colorMap[color]} stopOpacity="0"/>
              </linearGradient>
            </defs>
          </svg>
        </div>
      </div>
      
      <div className="summary-card-accent" style={{ background: colorMap[color] }}></div>
    </div>
  );
}

export default SummaryCard;