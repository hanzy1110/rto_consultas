#!/bin/sh
echo "Entrypoint..."
# source .env.prod
echo "Setting up database..."
python manage.py makemigrations --merge --noinput
python manage.py migrate --fake-initial rto_consultas
python manage.py collectstatic --noinput
python manage.py createsuperuser --no-input

sleep 10
echo "Starting Server..."

python manage.py runserver 0.0.0.0:${WEB_PORT}
