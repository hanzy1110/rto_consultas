CREATE USER 'replication_user'@'3.224.89.105' IDENTIFIED BY 'repl_pass2023';
GRANT REPLICATION SLAVE ON *.* TO 'replication_user'@'3.224.89.105';
FLUSH PRIVILEGES;
