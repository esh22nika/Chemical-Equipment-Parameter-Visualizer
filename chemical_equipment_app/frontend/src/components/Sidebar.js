import React from 'react';
import './Sidebar.css';

function Sidebar({ currentView, onViewChange }) {
  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: '📊' },
    { id: 'upload', label: 'Upload CSV', icon: '📤' },
    { id: 'data', label: 'Data Table', icon: '📋' },
    { id: 'history', label: 'History', icon: '🕒' },
    { id: 'report', label: 'Report', icon: '📄' },
  ];

  return (
    <aside className="sidebar">
      <ul className="menu">
        {menuItems.map((item) => (
          <li key={item.id}>
            <button
              className={`menu-item ${currentView === item.id ? 'active' : ''}`}
              onClick={() => onViewChange(item.id)}
            >
              <span className="menu-icon">{item.icon}</span>
              <span className="menu-label">{item.label}</span>
            </button>
          </li>
        ))}
      </ul>
    </aside>
  );
}

export default Sidebar;