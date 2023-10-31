#!/bin/bash
set -xe
source .env

SQL_INIT_DUMP_PATH=/home/ubuntu/git/rto_consultas/db_build/sql_init/a_vehicularunc_ultimo.sql
MYSQL_REPL_FILE=/home/ubuntu/git/rto_consultas/db_build/sql_init/e_repl_setup.sql
SQL_AZURE_DUMP_PATH=/home/ubuntu/central_dump
REMOTE_SERVER="azuresvr"
REMOTE_DUMP_PATH="/tmp/dump.sql"
# Local directory for dump file
LOCAL_DUMP_DIR="/home/ubuntu/central_dump/dump$(date +%F%T).sql"
# LOCAL_DUMP_FILE="dump.sql"
# MySQL dump command
MYSQLDUMP_CMD="mysqldump -u${MYSQL_DUMP_USER} -p${MYSQL_DUMP_PASSWORD} ${MYSQL_DATABASE}" >$REMOTE_DUMP_PATH
MYSQL_MASTER_CMD="mysql -u${MYSQL_DUMP_USER} -p${MYSQL_DUMP_PASSWORD} -e'show master status \G'"
MYSQL_FLUSH_CMD="mysql -u${MYSQL_DUMP_USER} -p${MYSQL_DUMP_PASSWORD} -e'flush tables with read lock \G'"
MYSQL_UNLOCK_CMD="mysql -u${MYSQL_DUMP_USER} -p${MYSQL_DUMP_PASSWORD} -e'unlock tables\G'"
# Define default values for flags
RELOAD=false
COPY=false

function copy_dump() {
    # Create a database dump on the remote server
    ssh $REMOTE_SERVER "${MYSQLDUMP_CMD}"
    # Copy the dump file to the local machine using rsync
    rsync -e "ssh" --partial --progress $REMOTE_SERVER:$REMOTE_DUMP_PATH $LOCAL_DUMP_DIR
    # Delete the dump file from the remote server
    ssh $REMOTE_SERVER "rm ${REMOTE_DUMP_PATH}"
    echo "Database dump copied and deleted from the remote server."
    return 0
}

function get_logfile_data() {
    ssh $REMOTE_SERVER $MYSQL_MASTER_CMD >"${HOME}/logfile.info"
    ssh $REMOTE_SERVER ${MYSQL_FLUSH_CMD} >"${HOME}/flush.info"

    cat "${HOME}/flush.info"

    mysql_out=$(cat "${HOME}/logfile.info")
    position=$(echo "$mysql_out" | awk '/Position:/{print $2}')
    log_file=$(echo "$mysql_out" | awk '/File:/{print $2}')

    echo "Position: $position"
    echo "Log File: $log_file"

    original_text=$(cat $MYSQL_REPL_FILE)

    modified_text=$(echo "$original_text" | sed -e "s/MASTER_LOG_FILE='[^']*'/MASTER_LOG_FILE='$log_file'/" -e "s/MASTER_LOG_POS=[0-9]*/MASTER_LOG_POS=$position/")
    echo "$modified_text" >$MYSQL_REPL_FILE

    return 0
}

function reload_db() {
    sudo docker-compose --env-file .env down --remove-orphans

    if [ "$1" = true ]; then
        sudo rm -rf sql_volume
        sudo cp $SQL_AZURE_DUMP_PATH/* $SQL_INIT_DUMP_PATH
        sudo rm ${SQL_AZURE_DUMP_PATH:?}/*
    fi
    sudo docker-compose --env-file .env build --no-cache
    sudo docker-compose --env-file .env up -d
    sudo docker-compose --env-file .env ps -a
    echo "Sleeping 5 min to allow db to start... then unlock!"
    sleep 300
    ssh $REMOTE_SERVER ${MYSQL_UNLOCK_CMD} >"${HOME}/unlock.info"
    sudo rm -rf "${HOME}/*.info"
    return 0
}
# Remote server details
# Parse command-line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -rc | --reload-copy)
            RELOAD=true
            COPY=true
            shift
            ;;
        -R | --rebuild)
            RELOAD=true
            shift
            ;;
        -r | --reload)
            RELOAD=true
            shift
            ;;
        -c | --copy)
            COPY=true
            shift
            ;;
        *)
            echo "Unknown argument: $1"
            exit 1
            ;;
    esac
done

# Check the flags and execute actions accordingly
if [ "$RELOAD" = true ] && [ "$COPY" = true ]; then
    echo "Getting Binary logfile and Position..."
    get_logfile_data ""
    set +x
    set +e
    echo "Copying dump..."
    copy_dump ""
    echo "Reloading database..." # Add code to copy the database dump here
    reload_db true
    # Add code to reload the database here
elif [ "$RELOAD" = true ]; then
    echo "Reloading database..."
    reload_db false
    # Add code to reload the database here
elif [ "$COPY" = true ]; then
    echo "Copying dump..."
    copy_dump ""
else # Add code to copy the database dump here
    echo "No flags provided. Use -r or --reload to reload the database, -c or --copy to copy the dump, or both."
fi
