# ChemFlow Analytics

A comprehensive chemical equipment parameter visualization and analysis platform available as both a **React Web Application** and a **PyQt5 Desktop Application**, powered by a shared Django REST backend.

## Overview

ChemFlow Analytics allows users to upload CSV files containing chemical equipment data (flowrate, pressure, temperature) and provides:

- Real-time data visualization with interactive charts
- Statistical analysis and insights
- Equipment type distribution analysis
- PDF report generation
- Upload history tracking
- Multi-platform support (Web & Desktop)

## Architecture

```
chemical_equipment_app/
├── backend/              # Django REST API (shared by both frontends)
├── frontend/             # React Web Application
└── desktop/              # PyQt5 Desktop Application
```

## Quick Start

### Prerequisites

- **Python 3.8+**
- **Node.js 14+** and npm (for React app)
- **pip** (Python package manager)

### Option 1: Automated Setup (Windows)

```bash
# Run the setup script
setup.bat
```

### Option 2: Manual Setup

#### 1. Backend Setup (Required for Both Apps)

```bash
# Create and activate virtual environment (from project root)
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r backend_requirements.txt

# Navigate to backend directory
cd backend

# Run migrations (from backend folder)
python manage.py makemigrations
python manage.py migrate

# Start the Django server (from backend folder)
python manage.py runserver
```

The backend will run on `http://localhost:8000`

#### 2a. React Web App Setup

```bash
# Navigate to frontend directory (from project root)
cd frontend

# Install dependencies (from frontend folder)
npm install

# Start the development server (from frontend folder)
npm start
```

The React app will open at `http://localhost:3000`

#### 2b. Desktop App Setup

```bash
# Activate the virtual environment (from project root)
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# Install desktop dependencies
pip install -r desktop_requirements.txt

# Navigate to desktop directory
cd desktop

# Run the desktop application (from desktop folder)
python main.py
```

## Dependencies

### Backend (Django)
- Django 5.0.1
- Django REST Framework 3.14.0
- django-cors-headers 4.3.1
- pandas 2.1.4
- reportlab 4.0.8
- Pillow 10.2.0

### Frontend (React)
- React 18+
- React Router DOM
- Chart.js & react-chartjs-2
- Axios
- jsPDF & html2canvas

### Desktop (PyQt5)
- PyQt5 5.15.10
- matplotlib 3.8.2
- requests 2.31.0

## Features

### Common Features (Both Apps)

1. **User Authentication**
   - Register new accounts
   - Login/Logout functionality

2. **Data Upload**
   - CSV file upload with validation
   - Required columns: Equipment Name, Type, Flowrate, Pressure, Temperature

3. **Analytics Dashboard**
   - Real-time parameter visualization
   - Interactive charts (line, bar, pie, radar)
   - Statistical analysis
   - Equipment type distribution

4. **Data Management**
   - View uploaded datasets
   - Upload history (last 5 datasets)
   - Delete datasets

5. **Report Generation**
   - PDF report creation
   - Download reports

### Web App Specific Features
- Responsive design
- Modern UI with animations
- Browser-based accessibility

### Desktop App Specific Features
- Native desktop integration
- Offline-first design
- Professional Qt-based UI

## CSV File Format

Your CSV file should have the following structure:

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-1,Pump,120,5.2,110
Compressor-1,Compressor,95,8.4,95
Valve-1,Valve,60,4.1,105
HeatExchanger-1,HeatExchanger,150,6.2,130
```

**Required Columns:**
- `Equipment Name` - Name/ID of the equipment
- `Type` - Equipment category (Pump, Compressor, Valve, etc.)
- `Flowrate` - Flow rate value (numeric)
- `Pressure` - Pressure value (numeric)
- `Temperature` - Temperature value (numeric)

A sample CSV file is provided at `sample_equipment_data.csv`

## Usage Guide

### First Time Setup

1. Start the Django backend server (required for both apps)
2. Choose your preferred interface:
   - **Web**: Start the React app
   - **Desktop**: Launch the PyQt5 application

### Creating an Account

1. Open the application (web or desktop)
2. Click "Create Account"
3. Enter username and password
4. Login with your credentials

### Uploading Data

1. Navigate to "Upload Data" tab
2. Click "Choose File" or drag-and-drop your CSV file
3. Click "Upload and Analyze"
4. View results in the Dashboard

### Viewing Analytics

The Dashboard displays:
- Summary statistics (total count, averages)
- Parameter trends (line chart)
- Equipment distribution (pie chart)
- Comparative analysis (bar chart)
- Statistical overview table

### Generating Reports

1. Navigate to "Reports" tab
2. Review the report preview
3. Click "Download PDF Report"
4. Save the PDF to your desired location

## Configuration

### Backend Settings

Edit `backend/backend/settings.py` to configure:

- Database settings (default: SQLite)
- CORS allowed origins
- Authentication settings
- Media file locations

### Frontend Settings

React app configuration in `frontend/src/services/api.js`:

```javascript
const API_BASE_URL = 'http://localhost:8000/api';
```

Desktop app configuration in `desktop/services/api_service.py`:

```python
self.base_url = "http://localhost:8000/api"
```

## Troubleshooting

### Backend Issues

**Port 8000 already in use:**
```bash
# Find and kill the process
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

**Database errors:**
```bash
# Delete db.sqlite3 and migrations, then re-run
python manage.py makemigrations
python manage.py migrate
```

### Frontend Issues

**React app won't start:**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

**CORS errors:**
- Ensure backend CORS settings include your frontend URL
- Check that backend is running on port 8000

### Desktop App Issues

**Import errors:**
```bash
# Ensure virtual environment is activated and dependencies installed
pip install -r desktop_requirements.txt
```

**Connection errors:**
- Verify Django backend is running
- Check firewall settings

## Application Screenshots

### React Web App
- Modern, responsive interface
- Interactive dashboards
- Mobile-friendly design

### Desktop App
- Native OS integration
- Professional PyQt5 UI
- Optimized for desktop workflows

## Security Notes

- Change `SECRET_KEY` in production
- Set `DEBUG = False` for production
- Use environment variables for sensitive data
- Implement proper user authentication
- Use HTTPS in production

## Contributing

This is a demonstration project. Feel free to fork and customize for your needs.

## License

This project is provided as-is for educational and demonstration purposes.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the code documentation
3. Ensure all dependencies are correctly installed

## Technical Details

### Backend API Endpoints

- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `POST /api/upload/` - Upload CSV file
- `GET /api/datasets/<id>/` - Get dataset details
- `GET /api/summary/<id>/` - Get dataset summary
- `GET /api/history/` - Get upload history
- `DELETE /api/datasets/<id>/` - Delete dataset
- `GET /api/datasets/<id>/download_pdf/` - Download PDF report

### Data Models

**Dataset Model:**
- filename
- upload_date
- total_count
- avg_flowrate, avg_pressure, avg_temperature
- equipment_type_distribution (JSON)
- data (JSON)

**Equipment Model:**
- equipment_name
- equipment_type
- flowrate, pressure, temperature
- Foreign key to Dataset

ent Analysis**
