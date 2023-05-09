#!/bin/sh
echo "Entrypoint..."
# source .env.prod
echo "Setting up database..."
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --no-input

sleep 10
echo "Starting Server..."

#  python manage.py collectstatic
# Start the Django development server with watchdog
watchmedo auto-restart --directory=./ --pattern=*.py --recursive -- \
    python manage.py runserver 0.0.0.0:8000

# python manage.py runserver 0.0.0.0:${WEB_PORT}
