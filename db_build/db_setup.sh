mysql -u root -p${MYSQL_ROOT_PASSWORD} -e "CREATE USER ${MYSQL_USER}@central_mysql_db IDENTIFIED BY ${MYSQL_PASSWORD} GRANT ALL PRIVILEGES ON *.* TO ${MYSQL_USER}@central_mysql_db WITH GRANT OPTION"
mysql -u root -p${MYSQL_ROOT_PASSWORD} -e "CREATE DATABASE ${MYSQL_DATABASE}"
# mysql -u root centralnqn < /app/ScriptSQL/centralNqn_210504.sql
