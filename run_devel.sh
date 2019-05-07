#!/bin/sh
python3 manage.py migrate --run-syncdb
python3 manage.py runserver 0.0.0.0:8000
