#!/usr/bin/env bash
# build.sh

echo "Collecting static files..."
python manage.py collectstatic --noinput