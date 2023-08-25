#!/bin/sh
docker-compose  --env-file .env down --remove-orphans
docker-compose  --env-file .env build --no-cache
docker-compose  --env-file .env up -d
docker-compose  --env-file .env ps -a

echo "Waiting for the bus"
# sleep 60
docker logs -t --follow central_mysql_db
docker logs -t central_mysql_exporter
# docker logs central_cron_mysql_bkp
# docker exec -it --env-file envfiles/.env central_site bash
