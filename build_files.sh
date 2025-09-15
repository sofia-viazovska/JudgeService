#!/bin/bash
# Build the project
echo "Building the project..."
python -m pip install -r requirements.txt

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Make directory for static files
mkdir -p staticfiles_build/static
mkdir -p staticfiles_build/static/judging
mkdir -p staticfiles_build/static/judging/css
mkdir -p staticfiles_build/static/judging/images

# Copy static files
cp -r static/ staticfiles_build/static/

# Copy CSS files
cp -r judging/static/judging/css/* staticfiles_build/static/judging/css/

# Copy image files
cp -r judging/static/judging/images/* staticfiles_build/static/judging/images/

echo "Build completed successfully!"
