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

RUN_LOGIN_INFO=""

echo "Do you wish to create or update MySQL login information? (y/n)"

read RUN_LOGIN_INFO

if [ ${RUN_LOGIN_INFO} = "y" -o "yes" ]; then
  echo "Running login_info.sh..."
  sh login_info.sh
else
  echo "Not generating MySQL login file"
fi

echo "Do you wish to create the required tables in your database?"

read CREATE_TABLES

if [ ${CREATE_TABLES} = "y" -o "yes" ]; then
  echo "Running make_tables.py..."
  python make_tables.py
else
  echo "Not creating tables"
fi

exit 0
