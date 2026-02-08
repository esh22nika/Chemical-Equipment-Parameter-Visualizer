@echo off
echo ========================================
echo Chemical Equipment Analyzer Setup
echo ========================================
echo.

echo Step 1: Setting up Backend...
echo.

REM Create virtual environment
python -m venv venv
call venv\Scripts\activate

REM Install backend dependencies
pip install -r backend_requirements.txt

REM Create necessary directories
if not exist "backend\backend" mkdir backend\backend
if not exist "backend\equipment" mkdir backend\equipment

echo.
echo Backend dependencies installed!
echo.

echo Step 2: Running migrations...
cd backend
python manage.py makemigrations
python manage.py migrate
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To run the application:
echo.
echo 1. Start Backend:
echo    cd backend
echo    python manage.py runserver
echo.
echo 2. Start Frontend (in new terminal):
echo    cd frontend
echo    npm install
echo    npm start
echo.
echo 3. Start Desktop App (in new terminal):
echo    venv\Scripts\activate
echo    cd desktop
echo    python main.py
echo.
pause