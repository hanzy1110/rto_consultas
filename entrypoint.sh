#!/bin/sh
echo "Entrypoint..."
# source .env.prod
echo "Setting up database..."
# sh -c "python manage.py migrate"
sh -c "python manage.py createsuperuser --no-input"

sleep 10
echo "Starting Server..."
sh -c "python manage.py runserver 0.0.0.0:${WEB_PORT}"
