#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Running database migrations..."
python manage.py migrate --no-input

#echo "Collecting static files..."
#python manage.py collectstatic --no-input

echo "Starting Gunicorn server..."
exec gunicorn be.wsgi:application --bind 0.0.0.0:8000