#!/usr/bin/env bash
# Render build script
# This script runs during deployment on Render

set -o errexit  # Exit on error

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Build completed successfully!"
echo "Note: Database migrations will run when the container starts"
