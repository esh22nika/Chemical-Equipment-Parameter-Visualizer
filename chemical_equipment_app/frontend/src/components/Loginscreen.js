import React, { useState } from 'react';
import { authService } from '../services/api';
import './LoginScreen.css';

function LoginScreen({ onLogin }) {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      if (isLogin) {
        const data = await authService.login(formData.username, formData.password);
        onLogin(data.token, data.user);
      } else {
        const data = await authService.register(
          formData.username,
          formData.email,
          formData.password
        );
        onLogin(data.token, data.user);
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Authentication failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-left">
        <div className="login-brand">
          <div className="brand-logo">
            <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
              <rect width="48" height="48" rx="12" fill="url(#login-gradient)" />
              <path
                d="M24 14L30 20H27V32H21V20H18L24 14Z"
                fill="white"
                opacity="0.95"
              />
              <circle cx="24" cy="36" r="3" fill="white" opacity="0.95" />
              <defs>
                <linearGradient id="login-gradient" x1="0" y1="0" x2="48" y2="48">
                  <stop offset="0%" stopColor="#0A6EBD" />
                  <stop offset="100%" stopColor="#00D4AA" />
                </linearGradient>
              </defs>
            </svg>
          </div>
          <div className="brand-info">
            <h1>ChemFlow</h1>
            <p>Equipment Analytics Platform</p>
          </div>
        </div>
        <div className="login-hero-graphic" aria-hidden="true">
          <svg width="520" height="300" viewBox="0 0 520 300" fill="none">
            <g opacity="0.9">
              <path d="M30 235C95 210 120 250 180 225C245 198 265 245 330 220C395 195 420 235 490 210" stroke="rgba(255,255,255,0.25)" strokeWidth="2" strokeDasharray="6 8"/>
              <path d="M24 255C88 230 120 270 176 248C240 224 266 262 328 240C392 218 424 250 488 228" stroke="rgba(0,212,170,0.3)" strokeWidth="2" strokeDasharray="4 10"/>
            </g>
            <g opacity="0.95">
              <circle cx="70" cy="90" r="10" fill="rgba(255,255,255,0.95)"/>
              <circle cx="120" cy="60" r="8" fill="rgba(0,212,170,0.95)"/>
              <circle cx="170" cy="105" r="9" fill="rgba(255,255,255,0.95)"/>
              <circle cx="230" cy="70" r="7" fill="rgba(0,212,170,0.9)"/>
              <circle cx="285" cy="115" r="10" fill="rgba(255,255,255,0.95)"/>
              <circle cx="340" cy="80" r="8" fill="rgba(0,212,170,0.9)"/>
              <circle cx="395" cy="120" r="9" fill="rgba(255,255,255,0.9)"/>
              <circle cx="455" cy="95" r="7" fill="rgba(0,212,170,0.9)"/>
              <circle cx="480" cy="150" r="10" fill="rgba(255,255,255,0.9)"/>
              <circle cx="410" cy="170" r="8" fill="rgba(0,212,170,0.85)"/>
              <circle cx="350" cy="155" r="7" fill="rgba(255,255,255,0.85)"/>
              <circle cx="300" cy="185" r="9" fill="rgba(0,212,170,0.85)"/>
              <circle cx="240" cy="160" r="7" fill="rgba(255,255,255,0.85)"/>
              <circle cx="190" cy="190" r="10" fill="rgba(0,212,170,0.9)"/>
              <circle cx="120" cy="170" r="8" fill="rgba(255,255,255,0.85)"/>
              <circle cx="60" cy="200" r="9" fill="rgba(0,212,170,0.85)"/>
              <path d="M78 88L112 66" stroke="rgba(255,255,255,0.6)" strokeWidth="2"/>
              <path d="M130 66L164 100" stroke="rgba(255,255,255,0.5)" strokeWidth="2"/>
              <path d="M176 102L222 74" stroke="rgba(255,255,255,0.45)" strokeWidth="2"/>
              <path d="M236 76L276 108" stroke="rgba(255,255,255,0.5)" strokeWidth="2"/>
              <path d="M292 110L332 84" stroke="rgba(255,255,255,0.45)" strokeWidth="2"/>
              <path d="M346 86L386 116" stroke="rgba(255,255,255,0.45)" strokeWidth="2"/>
              <path d="M404 122L448 98" stroke="rgba(255,255,255,0.4)" strokeWidth="2"/>
              <path d="M458 104L474 140" stroke="rgba(255,255,255,0.4)" strokeWidth="2"/>
              <path d="M468 154L418 168" stroke="rgba(255,255,255,0.4)" strokeWidth="2"/>
              <path d="M402 170L360 156" stroke="rgba(255,255,255,0.4)" strokeWidth="2"/>
              <path d="M348 160L306 182" stroke="rgba(255,255,255,0.4)" strokeWidth="2"/>
              <path d="M292 186L248 166" stroke="rgba(255,255,255,0.4)" strokeWidth="2"/>
              <path d="M234 170L196 188" stroke="rgba(255,255,255,0.4)" strokeWidth="2"/>
              <path d="M182 190L128 172" stroke="rgba(255,255,255,0.35)" strokeWidth="2"/>
              <path d="M114 174L70 198" stroke="rgba(255,255,255,0.35)" strokeWidth="2"/>
            </g>
          </svg>
        </div>

        <div className="login-features">
          <div className="feature-item">
            <div className="feature-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <path d="M9 11L12 14L22 4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M21 12V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H16" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </div>
            <div className="feature-content">
              <h3>Real-time Analysis</h3>
              <p>Monitor equipment parameters with live dashboards</p>
            </div>
          </div>

          <div className="feature-item">
            <div className="feature-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <rect x="3" y="3" width="7" height="7" rx="2" stroke="currentColor" strokeWidth="2"/>
                <rect x="14" y="3" width="7" height="7" rx="2" stroke="currentColor" strokeWidth="2"/>
                <rect x="3" y="14" width="7" height="7" rx="2" stroke="currentColor" strokeWidth="2"/>
                <rect x="14" y="14" width="7" height="7" rx="2" stroke="currentColor" strokeWidth="2"/>
              </svg>
            </div>
            <div className="feature-content">
              <h3>Advanced Visualizations</h3>
              <p>Interactive charts and statistical insights</p>
            </div>
          </div>

          <div className="feature-item">
            <div className="feature-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <path d="M14 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V20C4 20.5304 4.21071 21.0391 4.58579 21.4142C4.96086 21.7893 5.46957 22 6 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V8L14 2Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M14 2V8H20M16 13H8M16 17H8M10 9H8" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </div>
            <div className="feature-content">
              <h3>Automated Reports</h3>
              <p>Generate comprehensive PDF reports instantly</p>
            </div>
          </div>
        </div>
      </div>

      <div className="login-right">
        <div className="login-card">
          <div className="login-header">
            <h2>{isLogin ? 'Welcome Back' : 'Create Account'}</h2>
            <p>
              {isLogin
                ? 'Sign in to access your equipment analytics'
                : 'Get started with ChemFlow Analytics'}
            </p>
          </div>

          <form onSubmit={handleSubmit} className="login-form">
            <div className="form-group">
              <label htmlFor="username">Username</label>
              <input
                type="text"
                id="username"
                name="username"
                value={formData.username}
                onChange={handleChange}
                required
                className="form-input"
                placeholder="Enter your username"
              />
            </div>

            {!isLogin && (
              <div className="form-group">
                <label htmlFor="email">Email</label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                  className="form-input"
                  placeholder="Enter your email"
                />
              </div>
            )}

            <div className="form-group">
              <label htmlFor="password">Password</label>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                required
                className="form-input"
                placeholder="Enter your password"
              />
            </div>

            {error && <div className="alert alert-error">{error}</div>}

            <button type="submit" className="btn btn-primary btn-submit" disabled={loading}>
              {loading ? (
                <>
                  <div className="btn-spinner"></div>
                  {isLogin ? 'Signing in...' : 'Creating account...'}
                </>
              ) : (
                isLogin ? 'Sign In' : 'Create Account'
              )}
            </button>
          </form>

          <div className="login-footer">
            <button onClick={() => setIsLogin(!isLogin)} className="link-button">
              {isLogin
                ? "Don't have an account? Sign up"
                : 'Already have an account? Sign in'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default LoginScreen;
