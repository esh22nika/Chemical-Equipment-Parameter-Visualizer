import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginScreen from './components/Loginscreen';
import Dashboard from './components/Dashboard';
import UploadCSV from './components/UploadCSV';
import DataTable from './components/Datatable';
import History from './components/History';
import ReportPreview from './components/ReportPreview';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import './components/App.css';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [currentView, setCurrentView] = useState('dashboard');
  const [currentDataset, setCurrentDataset] = useState(null);

  useEffect(() => {
    // Check if user is already logged in
    const token = localStorage.getItem('token');
    if (token) {
      setIsAuthenticated(true);
    }
  }, []);

  const handleLogin = (token, user) => {
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(user));
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setIsAuthenticated(false);
    setCurrentView('dashboard');
  };

  const handleDatasetUpload = (dataset) => {
    setCurrentDataset(dataset);
    setCurrentView('dashboard');
  };

  if (!isAuthenticated) {
    return <LoginScreen onLogin={handleLogin} />;
  }

  return (
    <div className="app-container">
      <Navbar onLogout={handleLogout} />
      <div className="main-layout">
        <Sidebar currentView={currentView} onViewChange={setCurrentView} />
        <main className="content">
          {currentView === 'dashboard' && (
            <Dashboard dataset={currentDataset} />
          )}
          {currentView === 'upload' && (
            <UploadCSV onUploadSuccess={handleDatasetUpload} />
          )}
          {currentView === 'data' && (
            <DataTable dataset={currentDataset} />
          )}
          {currentView === 'history' && (
            <History onSelectDataset={setCurrentDataset} />
          )}
          {currentView === 'report' && (
            <ReportPreview dataset={currentDataset} />
          )}
        </main>
      </div>
    </div>
  );
}

export default App;
