#!/bin/bash
sleep 2 #

python manage.py makemigrations
python manage.py makemigrations accountingForCatsAndDoqsAPI
python manage.py migrate

exec "$@"