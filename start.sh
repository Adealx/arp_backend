#!/usr/bin/env bash
set -e

python manage.py collectstatic --no-input
python manage.py migrate
gunicorn arp_api.wsgi:application --bind 0.0.0.0:8000 --workers 2
