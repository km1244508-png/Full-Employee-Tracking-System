#!/bin/bash

# Quick Start Script for Mac/Linux
# This script sets up and runs the Attendance Tracking Application

echo ""
echo "========================================"
echo " Attendance & Work Progress Tracker"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi

echo "Python is installed ✓"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo "Dependencies installed ✓"
echo ""

# Start the app
echo "Starting Attendance Tracker..."
echo ""
echo "App will open in your browser at: http://localhost:8501"
echo ""
echo "Default Admin Credentials:"
echo "  Username: admin"
echo "  Password: admin123"
echo ""
echo "IMPORTANT: Change the admin password immediately!"
echo ""

streamlit run app.py
