#!/bin/bash
python manage.py migrate --noinput
gunicorn SIGLO.wsgi:application --bind 0.0.0.0:$PORT