#!/bin/sh
set -e

# Apply database migrations, collectstatic, then start gunicorn
echo "Running migrations..."
cd /app/JOB1 || exit 0
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn job1.wsgi:application --bind 0.0.0.0::${PORT} --workers 3
