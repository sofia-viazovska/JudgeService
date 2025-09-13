#!/bin/bash
# Build the project
echo "Building the project..."
python -m pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Make directory for static files
mkdir -p staticfiles_build/static
mkdir -p staticfiles_build/static/judging

# Copy static files
cp -r static/ staticfiles_build/static/
cp -r judging/static/judging/ staticfiles_build/static/judging/

echo "Build completed successfully!"
