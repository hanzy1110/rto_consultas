#!/bin/bash
# rm ./event_manager/migrations/*
echo "Working dir"

sudo docker-compose --env-file .env down --remove-orphans 
sudo docker-compose --env-file .env build --progress plain

echo MAKING AND APPLYING MIGRATIONS...
# sudo docker-compose --env-file v run --rm rto_consultas bash -c "python manage.py makemigrations && python manage.py migrate --fake-initial"
# sudo docker-compose --env-file .env run --rm crm_api sh -c "python manage.py migrate"

sudo docker-compose --env-file .env up -d 

echo "----------------------<>-----------------------"
echo Waiting for containers...
sleep 10
sudo docker ps -a 
sudo docker logs -tf rto_mysql_db
