#!/bin/bash
gunicorn SIGLO.wsgi:application --bind 0.0.0.0:$PORT