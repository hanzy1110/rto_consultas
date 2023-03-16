#!/bin/bash
# rm ./event_manager/migrations/*
echo "Working dir"
echo $(pwd)

sudo docker-compose --env-file envfiles/.env down --remove-orphans --rm all 
sudo docker-compose --env-file envfiles/.env build --progress plain

echo MAKING AND APPLYING MIGRATIONS...
sudo docker-compose --env-file envfiles/.env run --rm rto_consultas python manage.py makemigrations && python manage.py migrate
# sudo docker-compose --env-file .env run --rm crm_api sh -c "python manage.py migrate"

sudo docker-compose --env-file envfiles/.env up -d --force-recreate

echo Waiting for containers...
sleep 10
sudo docker ps -a 
sudo docker logs -t rto_mysql_db

echo "----------------------<>-----------------------"
sudo docker logs -t --follow rto_consultas

# sudo docker exec -it crm_api bash 

