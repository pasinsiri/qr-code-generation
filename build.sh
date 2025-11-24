#!/usr/bin/env bash
# Build script for Render deployment
# This script runs during the build phase to set up the database

set -o errexit  # Exit on error

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Initializing database..."
python init_db.py

echo "Build completed successfully!"
