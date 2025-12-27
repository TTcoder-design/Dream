#!/bin/bash

# Azure App Service startup script for Flask application
# This script is executed when the container starts

echo "Starting HOMOFLIXCINEMA Flask Application..."

# Install production dependencies if needed
echo "Ensuring dependencies are installed..."
pip install -r requirements.txt

# Start Gunicorn with optimized settings for Azure
echo "Starting Gunicorn server..."
gunicorn --bind=0.0.0.0:$PORT \
         --workers=2 \
         --threads=4 \
         --worker-class=gthread \
         --timeout=120 \
         --access-logfile=- \
         --error-logfile=- \
         --log-level=info \
         app:app
