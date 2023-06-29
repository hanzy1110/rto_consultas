#!/bin/bash
source ./envfiles/.env
dt=$(date '+%Y_%m_%d_%H_%M_%S_%6N');
echo "Sincronizando con servidor 02..."
RSYNC_LOG=/home/ubuntu/sql/log/rclone_${dt}.log
# Iterate the string array using for loop
# mv "$BACKUP_PATH/latest.${MYSQL_DATABASE}.sql.gz" "$BACKUP_PATH/${MYSQL_DATABASE}.${dt}.sql.gz"
rclone copy --config $RSYNC_CONFIG --contimeout 5m0s --log-file $RSYNC_LOG --log-level "DEBUG" --log-systemd --max-duration 86400s --max-size 488281 --retries 10 --retries-sleep 1m --use-json-log --create-empty-src-dirs $BACKUP_PATH $S3_USERNAME:${BUCKET_NAME}/backup_db 2>&1
# rm -rf $BACKUP_PATH/*
# Ver contenido en S3
# rclone tree --config envfiles/rclone.conf rto_static_replication_s3:rtobuckettest/22 > content.txt
chmod -R 777 $RSYNC_LOG
