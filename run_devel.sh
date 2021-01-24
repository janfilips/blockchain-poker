#!/bin/sh
python3 -m venv .venv
python3 manage.py migrate --run-syncdb
python3 manage.py runserver 0.0.0.0:8001
