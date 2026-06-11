#!/usr/bin/env bash
set -e

python manage.py collectstatic --no-input
# Fake-apply the legacy branch migrations so Django doesn't try to re-apply
# changes that were already made by the 0002_salesorder_multi_items branch.
python manage.py migrate sales 0003_add_approved_status --fake 2>/dev/null || true
python manage.py migrate
gunicorn arp_api.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2 --timeout 120 --keep-alive 5
