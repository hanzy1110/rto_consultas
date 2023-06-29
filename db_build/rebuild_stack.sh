#!/bin/sh
docker-compose  --env-file envfiles/.env down --remove-orphans
docker-compose  --env-file envfiles/.env build --no-cache
docker-compose  --env-file envfiles/.env up -d
docker-compose  --env-file envfiles/.env ps -a

echo "Waiting for the bus"
# sleep 60
docker logs -t --follow central_mysql_db
docker logs -t central_mysql_exporter
# docker logs central_cron_mysql_bkp
# docker exec -it --env-file envfiles/.env central_site bash
