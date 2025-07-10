#!/bin/bash

# Script to run the cities processor in a virtual environment
# This script activates the virtual environment and runs the Python script

echo "=== GeoNames Cities Data Processor ==="
echo "Activating virtual environment..."

# Check if virtual environment exists
if [ ! -d "cities_env" ]; then
    echo "Virtual environment not found. Creating it..."
    python3 -m venv cities_env
    echo "Virtual environment created successfully."
fi

# Activate virtual environment
source cities_env/bin/activate

echo "Virtual environment activated (Python $(python --version 2>&1))"
echo "Running cities processor..."
echo ""

# Run the Python script
python process_cities.py

echo ""
echo "=== Process Complete ==="
echo "Virtual environment: cities_env"
echo "Database file: cities.sqlite"
echo "To manually activate the environment, run: source cities_env/bin/activate"