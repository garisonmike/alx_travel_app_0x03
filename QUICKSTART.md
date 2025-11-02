# ALX Travel App - Quick Reference

## Quick Commands

### First Time Setup
```bash
./setup.sh
# OR manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed
```

### Daily Development
```bash
# Activate virtual environment
source venv/bin/activate

# Run server
python manage.py runserver

# Create superuser
python manage.py createsuperuser
```

### Database Operations
```bash
# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Seed sample data
python manage.py seed

# Reset database
rm db.sqlite3
python manage.py migrate
python manage.py seed
```

### Testing
```bash
# Run all tests
python manage.py test

# Run specific test
python manage.py test listings.tests.ListingModelTest

# Verbose output
python manage.py test --verbosity=2
```

## API Testing with curl

### Listings
```bash
# Get all listings
curl http://127.0.0.1:8000/api/listings/

# Get specific listing
curl http://127.0.0.1:8000/api/listings/{id}/

# Create listing
curl -X POST http://127.0.0.1:8000/api/listings/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Ocean View Villa",
    "description": "Stunning ocean views",
    "price_per_night": "250.00",
    "location": "Malibu"
  }'
```

### Bookings
```bash
# Create booking
curl -X POST http://127.0.0.1:8000/api/bookings/ \
  -H "Content-Type: application/json" \
  -d '{
    "user": 1,
    "listing": "listing-uuid-here",
    "start_date": "2025-11-01",
    "end_date": "2025-11-05"
  }'
```

### Reviews
```bash
# Create review
curl -X POST http://127.0.0.1:8000/api/reviews/ \
  -H "Content-Type: application/json" \
  -d '{
    "user": 1,
    "listing": "listing-uuid-here",
    "rating": 5,
    "comment": "Amazing place!"
  }'
```

## Access Points

- **API Root**: http://127.0.0.1:8000/api/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Listings**: http://127.0.0.1:8000/api/listings/
- **Bookings**: http://127.0.0.1:8000/api/bookings/
- **Reviews**: http://127.0.0.1:8000/api/reviews/

## Useful Django Commands

```bash
# Django shell
python manage.py shell

# Create migrations
python manage.py makemigrations

# Show migrations
python manage.py showmigrations

# SQL for migrations
python manage.py sqlmigrate listings 0001

# Check for issues
python manage.py check

# Collect static files
python manage.py collectstatic

# Database shell
python manage.py dbshell
```

## Project Statistics

```bash
# Count lines of code
find . -name '*.py' -not -path './venv/*' | xargs wc -l

# List all Python files
find . -name '*.py' -not -path './venv/*'

# Check Django version
python -m django --version
```

## Debugging

### Django Shell Examples
```python
# python manage.py shell

from listings.models import Listing, Booking, Review
from django.contrib.auth.models import User

# Get all listings
Listing.objects.all()

# Get listing count
Listing.objects.count()

# Filter listings
Listing.objects.filter(location="Mombasa")

# Create listing
listing = Listing.objects.create(
    title="Test House",
    description="A test property",
    price_per_night=100.00,
    location="Nairobi"
)

# Get user
user = User.objects.first()

# Create booking
booking = Booking.objects.create(
    user=user,
    listing=listing,
    start_date="2025-11-01",
    end_date="2025-11-05"
)
```

## Git Commands

```bash
# Check status
git status

# Add files
git add .

# Commit
git commit -m "Your message"

# Push
git push origin main

# View log
git log --oneline
```
