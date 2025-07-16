#!/bin/bash

# Script to run the D&D data scraper

echo "D&D Data Scraper for Seneschal"
echo "==============================="

# Check if running in Docker
if [ -f /.dockerenv ]; then
    echo "Running in Docker environment..."
    PYTHON_CMD="python"
else
    echo "Running in local environment..."
    # Try to use virtual environment if available
    if [ -d "../.venv" ]; then
        source ../.venv/bin/activate
        echo "Activated virtual environment"
    fi
    PYTHON_CMD="python"
fi

# Install requirements if needed
if [ ! -f "requirements_installed.flag" ]; then
    echo "Installing scraper dependencies..."
    $PYTHON_CMD -m pip install -r requirements.txt
    touch requirements_installed.flag
fi

# Run the scraper
echo "Starting D&D data scraping..."
$PYTHON_CMD scraper.py

# Check if scraping was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "Scraping completed successfully!"
    echo ""
    read -p "Would you like to import the scraped data into the database? (y/N): " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Importing data into database..."
        $PYTHON_CMD import_data.py
        
        if [ $? -eq 0 ]; then
            echo "Data import completed successfully!"
        else
            echo "Data import failed!"
            exit 1
        fi
    else
        echo "Skipping data import. You can run 'python import_data.py' later."
    fi
else
    echo "Scraping failed!"
    exit 1
fi

echo ""
echo "All operations completed!"
