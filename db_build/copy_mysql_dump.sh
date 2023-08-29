#!/bin/bash

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h | --help)
            echo "Usage: ./db_copy_script.sh -u remote_username -i remote_server_ip -p remote_dump_path -d local_dump_dir -f local_dump_file -U your_username -n your_database_name"
            exit 0
            ;;
        -u | --user)
            REMOTE_USER=$2
            shift
            shift
            ;;
        -i | --ip)
            REMOTE_SERVER=$2
            shift
            shift
            ;;
        -p | --path)
            REMOTE_DUMP_PATH=$2
            shift
            shift
            ;;
        -d | --dir)
            LOCAL_DUMP_DIR=$2
            shift
            shift
            ;;
        -f | --file)
            LOCAL_DUMP_FILE=$2
            shift
            shift
            ;;
        -U | --mysql-user)
            MYSQL_USER=$2
            shift
            shift
            ;;
        -n | --database-name)
            DATABASE_NAME=$2
            shift
            shift
            ;;
        *)
            echo "Unknown argument: $1. Use -h or --help for usage."
            exit 1
            ;;
    esac
done

# Check if required arguments are provided
if [ -z "$REMOTE_USER" ] || [ -z "$REMOTE_SERVER" ] || [ -z "$REMOTE_DUMP_PATH" ] || [ -z "$LOCAL_DUMP_DIR" ] || [ -z "$LOCAL_DUMP_FILE" ] || [ -z "$MYSQL_USER" ] || [ -z "$DATABASE_NAME" ]; then
    echo "Missing arguments. Use -h or --help for usage."
    exit 1
fi

# MySQL dump command
MYSQLDUMP_CMD="mysqldump -u $MYSQL_USER -p $DATABASE_NAME > $LOCAL_DUMP_DIR$LOCAL_DUMP_FILE"

# Create a database dump on the remote server
sshpass -p MpX6HyFY5m2w ssh $REMOTE_USER@$REMOTE_SERVER "$MYSQLDUMP_CMD"

# Copy the dump file to the local machine using rsync
rsync -e "ssh" --partial --progress "$REMOTE_USER"@"$REMOTE_SERVER":"$REMOTE_DUMP_PATH" "$LOCAL_DUMP_DIR"

# Delete the dump file from the remote server
ssh "$REMOTE_USER"@"$REMOTE_SERVER" "rm ${REMOTE_DUMP_PATH}"

echo "Database dump copied and deleted from the remote server."
