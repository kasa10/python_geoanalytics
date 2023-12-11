#!/bin/bash

# Подключение к MySQL и выполнение SQL-скриптов
mysql -h localhost -u root -p 11061978 geosurf < create_tables.sql
#mysql -h your_mysql_host -u your_mysql_user -p your_mysql_password your_database_name < insert_data.sql
