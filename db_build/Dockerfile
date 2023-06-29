FROM mysql/mysql-server:8.0
# Add crontab file in the cron directory
RUN apt-get update \  
  && apt-get install curl -y

RUN mkdir /envfiles
COPY ./envfiles /envfiles
ADD rcloneS3 /etc/cron.d/rcloneS3
ADD rclone.sh /

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/rcloneS3

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

#Install Cron
# RUN apt-get update
# RUN apt-get -y install cron

RUN curl https://rclone.org/install.sh | bash 

# Run the command on container startup
# CMD cron && tail -f /var/log/cron.log
