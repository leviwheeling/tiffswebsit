#!/bin/bash

# Start Duncan Family Dentistry Site Ping Script
# This script will ping duncanfamilydental.com every 10 minutes

echo "Starting Duncan Family Dentistry site ping monitor..."
echo "This will ping duncanfamilydental.com every 10 minutes"
echo "Press Ctrl+C to stop"
echo ""

# Check if we're in a virtual environment
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Virtual environment detected: $VIRTUAL_ENV"
else
    echo "⚠️  No virtual environment detected. Consider activating one:"
    echo "   source env/bin/activate"
    echo ""
fi

# Check if requests is installed
python3 -c "import requests" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ Required dependencies found"
else
    echo "❌ Missing required dependencies. Installing..."
    pip install requests
fi

echo ""
echo "Starting ping monitor..."
python3 ping_site.py
