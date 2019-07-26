#!/bin/bash
/usr/bin/python3 /usr/bin/manage.py migrate --noinput
/usr/bin/python3 /usr/bin/manage.py makemigrations --noinput
/usr/bin/python3 /usr/bin/manage.py makemigrations env --noinput
/usr/bin/python3 /usr/bin/manage.py migrate --noinput
/usr/bin/python3 /usr/bin/manage.py initialize_env
/usr/bin/python3 /usr/bin/manage.py install_cron 
/usr/bin/python3 /usr/bin/manage.py collectstatic --noinput

/usr/bin/uwsgi --ini /usr/bin/esmt.ini
