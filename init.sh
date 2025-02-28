#!/bin/bash
set -e

# Set the MySQL root password from the environment variable
if [ -z "$MYSQL_ROOT_PASSWORD" ]; then
    echo "MYSQL_ROOT_PASSWORD not set, using default password 'root'"
    MYSQL_ROOT_PASSWORD=root
fi

# Start MySQL
service mysql start

# Set the root password
mysql -u root -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '${MYSQL_ROOT_PASSWORD}';"