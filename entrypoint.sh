#!/bin/bash
sleep 2 #

python manage.py makemigrations
python manage.py migrate

exec "$@"