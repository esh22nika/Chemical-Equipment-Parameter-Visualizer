import React from 'react';
import './Navbar.css';

function Navbar({ onLogout }) {
  const user = JSON.parse(localStorage.getItem('user') || '{}');

  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <h1>🧪 Chemical Equipment Analyzer</h1>
      </div>
      <div className="navbar-user">
        <span>Welcome, {user.username || 'User'}</span>
        <button onClick={onLogout} className="logout-button">
          Logout
        </button>
      </div>
    </nav>
  );
}

export default Navbar;