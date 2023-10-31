#!/bin/sh
echo "Entrypoint..."
# source .env.prod
echo "Setting up database..."
python manage.py makemigrations rto_consultas --noinput
python manage.py migrate --fake-initial
python manage.py collectstatic --noinput
python manage.py createsuperuser --no-input --database users

sleep 10
echo "Starting Server..."

python manage.py runserver 0.0.0.0:${WEB_PORT}
