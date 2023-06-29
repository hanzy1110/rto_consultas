sudo cp rcloneS3 /etc/cron.d/rcloneS3
# Give execution rights on the cron job
chmod 0644 /etc/cron.d/rcloneS3
curl https://rclone.org/install.sh | bash 
chmod +x /home/ubuntu/rto_central_deploy/deploy/central_mysql_db/rclone.sh
