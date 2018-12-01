#!/bin/sh

echo "Enter the username of the MySQL account you wish to login with: "
read uname

stty -echo
echo "Enter the password of the MySQL account you wish to login with: "
read  password
stty echo

echo "Enter the name of the MySQL database you wish to use: "
read db_name

echo "'''\nA document containing MySQL login information for localhost.\n'''" > ../lib/mysql_login_info.py
echo "mysql_uname = '"$uname"'\n" >> ../lib/mysql_login_info.py
echo "mysql_pw = '"$password"'\n" >> ../lib/mysql_login_info.py
echo "mysql_db_name= '"$db_name"'" >> ../lib/mysql_login_info.py
