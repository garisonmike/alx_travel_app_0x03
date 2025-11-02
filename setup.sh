#!/bin/bash

# Setup script for ALX Travel App
echo "Setting up ALX Travel App..."

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Run migrations
echo "Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
echo ""
echo "Would you like to create a superuser for the admin panel?"
echo "   You can do this later with: python manage.py createsuperuser"
echo ""

# Seed database
echo "Seeding database with sample data..."
python manage.py seed

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "   1. Activate the virtual environment: source venv/bin/activate"
echo "   2. Create a superuser (optional): python manage.py createsuperuser"
echo "   3. Run the development server: python manage.py runserver"
echo "   4. Visit http://127.0.0.1:8000/api/ to see the API"
echo "   5. Visit http://127.0.0.1:8000/admin/ for the admin panel"
echo ""
