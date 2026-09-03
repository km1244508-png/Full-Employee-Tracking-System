@echo off
REM Quick Start Script for Windows
REM This script sets up and runs the Attendance Tracking Application

echo.
echo ========================================
echo  Attendance & Work Progress Tracker
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python is installed ✓
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo Dependencies installed ✓
echo.

REM Start the app
echo Starting Attendance Tracker...
echo.
echo App will open in your browser at: http://localhost:8501
echo.
echo Default Admin Credentials:
echo   Username: admin
echo   Password: admin123
echo.
echo IMPORTANT: Change the admin password immediately!
echo.
pause

streamlit run app.py

pause
