echo SHUTTING DOWN DB
docker-compose --env-file .env.prod down

echo DELETING VOLUMES
docker volume rm backend_crm_db_data
docker volume rm backend_pgadmin
