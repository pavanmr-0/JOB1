#!/bin/sh
set -e

# Apply database migrations, collectstatic, then start gunicorn
echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn job1.wsgi:application --bind 0.0.0.0:8000 --workers 3
