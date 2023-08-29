#!/bin/bash

# Remote server details
REMOTE_SERVER="azureSVR"
REMOTE_DUMP_PATH="/tmp/dump.sql"
MYSQL_USER="replication_user"
MYSQL_PASSWORD="repl_pass2023"

# Local directory for dump file
LOCAL_DUMP_DIR="/home/ubuntu/central_dump"
# LOCAL_DUMP_FILE="dump.sql"

# MySQL dump command
MYSQLDUMP_CMD="mysqldump -u ${MYSQL_USER} -p ${MYSQL_PASSWORD} > $REMOTE_DUMP_PATH"

# Create a database dump on the remote server
ssh $REMOTE_SERVER "${MYSQLDUMP_CMD}"

# Copy the dump file to the local machine using rsync
rsync -e "ssh" --partial --progress $REMOTE_SERVER:$REMOTE_DUMP_PATH $LOCAL_DUMP_DIR

# Delete the dump file from the remote server
ssh $REMOTE_SERVER "rm ${REMOTE_DUMP_PATH}"

echo "Database dump copied and deleted from the remote server."
