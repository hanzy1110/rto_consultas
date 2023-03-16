#!/bin/bash
# rm ./event_manager/migrations/*
echo "Working dir"
echo $(pwd)

docker-compose --env-file .env down --remove-orphans
docker-compose --env-file .env build

echo MAKING AND APPLYING MIGRATIONS...
docker-compose --env-file .env run --rm rto_consultas -c "python manage.py makemigrations && python manage.py migrate"
# docker-compose --env-file .env run --rm crm_api sh -c "python manage.py migrate"

docker-compose --env-file .env up -d 

echo Waiting for containers...
sleep 10
docker ps -a 
docker logs -t rto_mysql_db

echo "----------------------<>-----------------------"
docker logs -t --follow rto_consultas

# docker exec -it crm_api bash 

