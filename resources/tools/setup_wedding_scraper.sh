#!/bin/bash
# Setup script for Wedding Venue Scraper
# This script installs dependencies and runs a quick test

echo "======================================================================"
echo "Wedding Venue Scraper - Setup Script"
echo "======================================================================"
echo ""

# Check Python installation
echo "🔍 Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
    echo "✅ Python3 found: $(python3 --version)"
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
    echo "✅ Python found: $(python --version)"
else
    echo "❌ Python not found. Please install Python 3.8 or higher."
    exit 1
fi

# Check pip installation
echo ""
echo "🔍 Checking pip installation..."
if command -v pip3 &> /dev/null; then
    PIP_CMD=pip3
    echo "✅ pip3 found"
elif command -v pip &> /dev/null; then
    PIP_CMD=pip
    echo "✅ pip found"
else
    echo "❌ pip not found. Please install pip."
    exit 1
fi

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
$PIP_CMD install -r requirements_wedding_scraper.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Verify Selenium installation
echo ""
echo "🔍 Verifying Selenium installation..."
$PYTHON_CMD -c "import selenium; print('✅ Selenium version:', selenium.__version__)" 2>/dev/null

if [ $? -ne 0 ]; then
    echo "❌ Selenium verification failed"
    exit 1
fi

# Setup complete
echo ""
echo "======================================================================"
echo "✅ Setup Complete!"
echo "======================================================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Test the scraper with a single city:"
echo "   $PYTHON_CMD test_wedding_scraper.py"
echo ""
echo "2. Run the full scraper (489 cities, several hours):"
echo "   $PYTHON_CMD wedding_venue_scraper.py"
echo ""
echo "3. Check the README for more options:"
echo "   cat README_wedding_scraper.md"
echo ""
echo "💡 Tip: Run the test script first to verify everything works!"
echo ""
