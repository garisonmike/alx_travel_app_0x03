#!/bin/sh
set -e

echo "Starting entrypoint script..."

# Wait for database to be ready
if [ "$DATABASE_URL" ]; then
    echo "Waiting for PostgreSQL..."
    
    # Extract host and port from DATABASE_URL
    DB_HOST=$(echo $DATABASE_URL | sed -n 's/.*@\([^:]*\):.*/\1/p')
    DB_PORT=$(echo $DATABASE_URL | sed -n 's/.*:\([0-9]*\)\/.*/\1/p')
    
    if [ -z "$DB_PORT" ]; then
        DB_PORT=5432
    fi
    
    while ! nc -z $DB_HOST $DB_PORT; do
        echo "PostgreSQL is unavailable - sleeping"
        sleep 1
    done
    
    echo "PostgreSQL is up - continuing..."
fi

# Wait for RabbitMQ
if [ "$CELERY_BROKER_URL" ]; then
    echo "Waiting for RabbitMQ..."
    RABBITMQ_HOST=$(echo $CELERY_BROKER_URL | sed -n 's/.*@\([^:]*\):.*/\1/p')
    RABBITMQ_PORT=$(echo $CELERY_BROKER_URL | sed -n 's/.*:\([0-9]*\)\/.*/\1/p')
    
    if [ -z "$RABBITMQ_PORT" ]; then
        RABBITMQ_PORT=5672
    fi
    
    while ! nc -z $RABBITMQ_HOST $RABBITMQ_PORT; do
        echo "RabbitMQ is unavailable - sleeping"
        sleep 1
    done
    
    echo "RabbitMQ is up - continuing..."
fi

# Wait for Redis
if [ "$REDIS_URL" ]; then
    echo "Waiting for Redis..."
    REDIS_HOST=$(echo $REDIS_URL | sed -n 's/.*:\/\/\([^:]*\):.*/\1/p')
    REDIS_PORT=$(echo $REDIS_URL | sed -n 's/.*:\([0-9]*\).*/\1/p')
    
    if [ -z "$REDIS_PORT" ]; then
        REDIS_PORT=6379
    fi
    
    while ! nc -z $REDIS_HOST $REDIS_PORT; do
        echo "Redis is unavailable - sleeping"
        sleep 1
    done
    
    echo "Redis is up - continuing..."
fi

# Run migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create superuser if it doesn't exist (optional, for development)
if [ "$DJANGO_SUPERUSER_USERNAME" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ] && [ "$DJANGO_SUPERUSER_EMAIL" ]; then
    echo "Creating superuser..."
    python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')
    print('Superuser created successfully')
else:
    print('Superuser already exists')
EOF
fi

echo "Entrypoint script completed successfully"

# Execute the main command
exec "$@"
