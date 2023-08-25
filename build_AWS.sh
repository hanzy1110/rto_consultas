#!/bin/bash
# rm ./event_manager/migrations/*
echo "Working dir"

sudo docker-compose --env-file envfiles/.env down --remove-orphans
sudo docker-compose --env-file envfiles/.env build --progress plain

echo MAKING AND APPLYING MIGRATIONS...
sudo docker-compose --env-file envfiles/.env run --rm rto_consultas bash -c "python manage.py makemigrations && python manage.py migrate --fake-initial"
# sudo docker-compose --env-file .env run --rm crm_api sh -c "python manage.py migrate"

sudo docker-compose --env-file envfiles/.env up -d

echo "----------------------<>-----------------------"
echo Waiting for containers...
sleep 10
sudo docker ps -a
sudo docker logs -t rto_mysql_db

echo "----------------------<>-----------------------"
sudo docker logs -t --follow rto_consultas

# sudo docker exec -it crm_api bash
