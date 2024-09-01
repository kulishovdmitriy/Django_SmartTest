#!/bin/bash

echo "Waiting for PostgreSQL to be ready..."

sleep 5

echo "Running Django with ALLOWED_HOSTS: $ALLOWED_HOSTS"

python project/manage.py runserver 0:"${PORT}" --settings="app.settings.${RUN_MODE}"