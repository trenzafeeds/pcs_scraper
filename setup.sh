#!/bin/sh
#
#setup
#

PIP_FLAG=""
QUIET=0

while [ "$1" ]; do
  case "$1" in
    '-q') PIP_FLAG='-q'; QUIET=1;;
    *)    echo "$0: error: unknown arg"; exit 1;;
  esac
  shift
done

[ "$QUIET" -ne 1 ] && echo "Installing Python2 modules..."

sudo -H pip ${PIP_FLAG} install unidecode
sudo -H pip ${PIP_FLAG} install peewee
sudo -H pip ${PIP_FLAG} install beautifulsoup4

REP="t"

RUN_LOGIN_INFO=""

echo "Do you wish to create or update MySQL login information? (y/n)"

while [ ${REP} ]; do
  read RUN_LOGIN_INFO

  case "$RUN_LOGIN_INFO" in
    "yes"|"y")  echo "Running login_info.sh..."; sh bin/login_info.sh; REP="";;
    "no"|"n"|"c")  echo "Not generating MySQL login file"; REP=""; RUN_LOGIN_INFO="";;
    *) echo "invalid option: ${RUN_LOGIN_INFO}. Please answer with y or n.";;
  esac
done

REP="t"

echo "Do you wish to create the required tables in your database? (y/n) NOTE: Will not work without first creating MySQL login information file."

while [ ${REP} ]; do
  read CREATE_TABLES

  case "$CREATE_TABLES" in
    "yes"|"y")  echo "Running make_tables.py..."; python lib/make_tables.py; REP="";;
    "no"|"n")  echo "Not creating tables"; REP=""; CREATE_TABLES="";;
    *) echo "invalid option: ${RUN_LOGIN_INFO}. Please answer with y or n.";;
  esac
done

echo "\n"
echo "Setup complete!"
echo "Verified installation of:\nunidecode\npeewee\nbeautifulsoup4"
if [ ${RUN_LOGIN_INFO} ]; then
  echo "Updated lib/mysql_login_info.py"
fi

if [ ${CREATE_TABLES} ]; then
  echo "Created tables in MySQL database"
fi
exit 0
