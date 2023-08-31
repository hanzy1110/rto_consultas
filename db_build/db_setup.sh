set -xe

mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -e "CREATE USER exporter@rto_mysql_db IDENTIFIED BY ${MYSQL_PASSWORD} GRANT ALL PRIVILEGES ON *.* TO exporter@rto_mysql_db WITH GRANT OPTION"
mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -e "FLUSH PRIVILEGES"
# mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -e "CREATE DATABASE ${MYSQL_DATABASE}"

mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -e "CHANGE MASTER TO \
MASTER_HOST=40.87.111.221,
MASTER_USER='replication_user',
MASTER_PASSWORD='repl_pass2023',
MASTER-LOG-FILE=mysql-bin.000009
MASTER-LOG-POS=181968
"
# mysql -u root centralnqn < /app/ScriptSQL/centralNqn_210504.sql
