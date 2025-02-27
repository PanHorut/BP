#!/bin/bash
set -e

echo "Running database migrations..."
python /app/manage.py migrate --no-input

# If you're collecting static files, adjust this as well
# echo "Collecting static files..."
# python /app/manage.py collectstatic --no-input

echo "Starting Uvicorn server..."
DJANGO_SETTINGS_MODULE=be.settings uvicorn be.asgi:application --host 127.0.0.1 --port 8000 --reload
