#!/bin/bash

# Social Engineering Toolkit Startup Script

echo "===========================================" 
echo "  Social Engineering Toolkit (SET)"
echo "  Security Awareness Training Platform"
echo "==========================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3.7 or higher."
    exit 1
fi

# Check if setup has been run
if [ ! -f "data/setoolkit.db" ]; then
    echo "⚠️  Database not found. Running setup..."
    python setup.py
    if [ $? -ne 0 ]; then
        echo "❌ Setup failed. Please check the error messages above."
        exit 1
    fi
fi

echo "✅ Starting Social Engineering Toolkit..."
echo "📍 Access the application at: http://localhost:5000"
echo "👤 Demo Login - Admin: admin@company.com / admin123"
echo "👤 Demo Login - User: user@company.com / user123"
echo ""
echo "Press Ctrl+C to stop the server"
echo "==========================================="

# Start the Flask application
cd src
python app.py

