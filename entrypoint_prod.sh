#!/bin/sh
echo "Entrypoint..."
# source .env.prod
echo "Setting up database..."
python manage.py makemigrations rto_consultas --noinput
python manage.py migrate --database users --no-input
python manage.py collectstatic --noinput
python manage.py createsuperuser --database users --no-input

sleep 10
echo "Starting Server..."
# python manage.py runserver 0.0.0.0:${WEB_PORT}
python -m gunicorn -b "0.0.0.0:${WEB_PORT}" --worker-class=gevent --worker-connections=1000 --workers=3 rto_consultas.wsgi:application
