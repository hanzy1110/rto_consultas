#!/bin/bash
set -xe
git pull

sudo docker-compose --env-file envfiles/.env down --remove-orphans
sudo docker-compose --env-file envfiles/.env build

echo MAKING AND APPLYING MIGRATIONS...
# sudo docker-compose --env-file envfiles/.env run --rm rto_consultas bash -c "python manage.py makemigrations && python manage.py migrate --fake-initial"
# sudo docker-compose --env-file .env run --rm crm_api sh -c "python manage.py migrate"

sudo docker-compose --env-file envfiles/.env up -d

echo "----------------------<>-----------------------"
echo Waiting for containers...
sleep 10
sudo docker ps -a

# sudo docker exec -it crm_api bash
