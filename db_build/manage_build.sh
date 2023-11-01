#!/bin/bash
set -xe
source .env

SQL_INIT_RN=/home/ubuntu/git/rto_consultas/db_build/sql_init/rionegro
SQL_INIT_NQN=/home/ubuntu/git/rto_consultas/db_build/sql_init

SQL_INIT_DUMP_NQN=$SQL_INIT_NQN/a_vehicularunc_ultimo.sql
SQL_INIT_DUMP_RN=$SQL_INIT_RN/a_vtvrionegro_ultimo.sql

MYSQL_REPL_NQN=$SQL_INIT_NQN/e_repl_setup.sql
MYSQL_REPL_RN=$SQL_INIT_RN/e_repl_setup.sql

# DATABASE VOLUMES
MYSQL_NQN_VOLUME=/home/ubuntu/git/rto_consultas/db_build/sql_volume
POSTGRES_VOLUME=/home/ubuntu/git/rto_consultas/db_build/postgres_volume
MYSQL_RN_VOLUME=/home/ubuntu/git/rto_consultas/db_build/postgres_volume

SQL_AZURE_DUMP_PATH=/home/ubuntu/central_dump
REMOTE_SERVER="azuresvr"
REMOTE_DUMP_PATH="/tmp/dump.sql"

# Local directory for dump file
LOCAL_DUMP_DIR="/home/ubuntu/central_dump/dump$(date +%F%T).sql"
# LOCAL_DUMP_FILE="dump.sql"

# MySQL dump command
MYSQL_MASTER_CMD="mysql -u${MYSQL_DUMP_USER} -p${MYSQL_DUMP_PASSWORD} -e'show master status \G'"
MYSQL_FLUSH_CMD="mysql -u${MYSQL_DUMP_USER} -p${MYSQL_DUMP_PASSWORD} -e'flush tables with read lock \G'"
MYSQL_UNLOCK_CMD="mysql -u${MYSQL_DUMP_USER} -p${MYSQL_DUMP_PASSWORD} -e'unlock tables\G'"

# Define default values for flags
RELOAD_USERS=false
RELOAD_RN=false
RELOAD_ALL=false

function copy_dump() {

    MYSQLDUMP_CMD="mysqldump -u${MYSQL_DUMP_USER} -p${MYSQL_DUMP_PASSWORD} $1 >$REMOTE_DUMP_PATH"
    ssh $REMOTE_SERVER "${MYSQLDUMP_CMD}"
    rsync -e "ssh" --partial --progress $REMOTE_SERVER:$REMOTE_DUMP_PATH $LOCAL_DUMP_DIR
    ssh $REMOTE_SERVER "rm ${REMOTE_DUMP_PATH}"

    # Kinda meaningless
    if [ $? = 0 ]; then
        echo "Database dump copied and deleted from the remote server."
    fi

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

    if [ "$1" = "vehicularunc" ]; then
        echo "$modified_text" >$MYSQL_REPL_NQN
    elif [ "$1" = "vtvrionegro" ]; then
        echo "$modified_text" >$MYSQL_REPL_RN
    fi

    return 0
}

function reload_db() {

    if [ "$1" = "vehicularunc" ]; then
        sudo docker-compose --env-file .env rm -sv --force rto_mysql_db
        sudo rm -rf "$MYSQL_NQN_VOLUME"
        sudo cp $SQL_AZURE_DUMP_PATH/* $SQL_INIT_DUMP_NQN
        sudo rm ${SQL_AZURE_DUMP_PATH:?}/*
    elif [ "$1" = "vtvrionegro" ]; then
        sudo docker-compose --env-file .env rm -sv --force rto_rn_db
        sudo rm -rf "$MYSQL_RN_VOLUME"
        sudo cp $SQL_AZURE_DUMP_PATH/* $SQL_INIT_DUMP_RN
        sudo rm ${SQL_AZURE_DUMP_PATH:?}/*
    fi
    sudo docker-compose --env-file .env build --no-cache
    sudo docker-compose --env-file .env up -d
    sudo docker-compose --env-file .env ps -a

    return 0
}

function db_reload() {

    sudo docker-compose --env-file .env rm -sv --force "$2"

    if [ "$1" = true ]; then
        sudo rm -rf "$3"
    fi

    sudo docker-compose --env-file .env build "$2" --no-cache
    sudo docker-compose --env-file .env up -d "$2"
    sudo docker-compose --env-file .env ps -a
    return 0
}

function reload_RN() {

    echo "Getting Binary logfile and Position..."
    get_logfile_data "vtvrionegro"
    set +x
    set +e

    echo "Copying dump..."
    copy_dump "vtvrionegro"
    echo "Reloading database..."
    reload_db "vtvrionegro"

    return 0
}
#

function reload_NQN() {

    echo "Getting Binary logfile and Position..."
    get_logfile_data "vehicularunc"
    # set +x
    # set +e

    echo "Copying dump..."
    copy_dump "vehicularunc"
    echo "Reloading database..."
    reload_db "vehicularunc"

    return 0
}

function check_repl_status() {

    if [ "$1" = "vehicularunc" ]; then
        sudo docker exec rto_mysql_db "mysql -uroot -p123 -e'show slave status \G'" 2>&1 | sudo tee NQN.repl
    elif [ "$1" = "vtvrionegro" ]; then
        sudo docker exec rto_rn_db "mysql -uroot -p123 -e'show slave status \G'" 2>&1 | sudo tee RN.repl
    fi

    return 0
}
# Remote server details
# Parse command-line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -R | --reload-nqn)
            RELOAD_NQN=true
            shift
            ;;
        -U | --reload-users)
            RELOAD_USERS=true
            shift
            ;;
        -RN | --reload-rn)
            RELOAD_RN=true
            shift
            ;;
        -RA | --reload-all)
            RELOAD_ALL=true
            shift
            ;;
        *)
            echo "Unknown argument: $1"
            exit 1
            ;;
    esac
done

# Check the flags and execute actions accordingly
if [ "$RELOAD_NQN" = true ]; then
    reload_NQN "" 2>&1 | sudo tee ./NQN.log

    echo "Sleeping 5 min to allow db to start... then unlock!"
    sleep 300
    ssh $REMOTE_SERVER ${MYSQL_UNLOCK_CMD} >"${HOME}/unlock.info"
    cat ${HOME}/unlock.info
    sudo rm -rf "${HOME}/*.info"

    check_replication "vehicularunc"

elif [ "$RELOAD_USERS" = true ]; then
    echo "Reloading user db..."
    db_reload true rto_user_db $POSTGRES_VOLUME

elif [ "$RELOAD_RN" = true ]; then
    reload_RN "" 2>&1 | sudo tee ./RN.log

    echo "Sleeping 5 min to allow db to start... then unlock!"
    sleep 300
    ssh $REMOTE_SERVER ${MYSQL_UNLOCK_CMD} >"${HOME}/unlock.info"
    cat ${HOME}/unlock.info
    sudo rm -rf "${HOME}/*.info"
    check_replication "vtvrionegro"

elif [ "$RELOAD_ALL" = true ]; then
    reload_NQN "" 2>&1 | sudo tee ./NQN.log
    reload_RN "" 2>&1 | sudo tee ./RN.log

    echo "Sleeping 7 min to allow db to start... then unlock!"
    sleep 420
    ssh $REMOTE_SERVER ${MYSQL_UNLOCK_CMD} >"${HOME}/unlock.info"
    cat ${HOME}/unlock.info
    sudo rm -rf "${HOME}/*.info"
    check_replication "vtvrionegro"
    check_replication "vehicularunc"

else
    echo "No flags provided. Use -r or --reload to reload the database, -c or --copy to copy the dump, or both."
fi
