#!/bin/bash

# Social Engineering Toolkit Installation Script

echo "===========================================" 
echo "  Social Engineering Toolkit (SET)"
echo "  Installation Script"
echo "==========================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Installing Python 3..."
    sudo apt update && sudo apt install -y python3 python3-pip
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Installing pip3..."
    sudo apt install -y python3-pip
fi

echo "✅ Python dependencies check complete"

# Install Python packages
echo "Installing required Python packages..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "⚠️  Failed to install some packages. Trying with user flag..."
    pip3 install --user -r requirements.txt
fi

# Run setup
echo "Running initial setup..."
python3 setup.py

if [ $? -eq 0 ]; then
    echo "✅ Installation completed successfully!"
    echo ""
    echo "To start the Social Engineering Toolkit:"
    echo "  ./start.sh"
    echo ""
    echo "Or manually:"
    echo "  cd src && python3 app.py"
    echo ""
    echo "Then open your browser to: http://localhost:5000"
    echo ""
    echo "Demo credentials:"
    echo "  Admin: admin@company.com / admin123"
    echo "  User:  user@company.com / user123"
else
    echo "❌ Installation failed. Please check the error messages above."
    exit 1
fi

