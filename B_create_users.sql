CREATE USER 'exporter'@'rto_mysql_db' IDENTIFIED BY '123';
GRANT PROCESS, REPLICATION CLIENT ON *.* TO 'exporter'@'rto_mysql_db';
GRANT SELECT ON performance_schema.* TO 'exporter'@'rto_mysql_db';
FLUSH PRIVILEGES;

