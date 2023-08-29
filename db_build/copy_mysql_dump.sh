#!/bin/bash
set -xe

source .env

# Remote server details
REMOTE_SERVER="azureSVR"
REMOTE_DUMP_PATH="/tmp/dump.sql"

# Local directory for dump file
LOCAL_DUMP_DIR="/home/ubuntu/central_dump/dump$(date +%F%T).sql"
# LOCAL_DUMP_FILE="dump.sql"

# MySQL dump command
MYSQLDUMP_CMD="mysqldump -u ${MYSQL_DUMP_USER} -p${MYSQL_DUMP_PASSWORD} ${MYSQL_DATABASE} > $REMOTE_DUMP_PATH"

# Create a database dump on the remote server
ssh $REMOTE_SERVER "${MYSQLDUMP_CMD}"

# Copy the dump file to the local machine using rsync
rsync -e "ssh" --partial --progress $REMOTE_SERVER:$REMOTE_DUMP_PATH $LOCAL_DUMP_DIR

# Delete the dump file from the remote server
ssh $REMOTE_SERVER "rm ${REMOTE_DUMP_PATH}"

echo "Database dump copied and deleted from the remote server."
