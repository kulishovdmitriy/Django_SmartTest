#!/bin/bash

echo "Waiting for PostgreSQL to be ready..."

sleep 5

echo "Starting Django server..."

python project/manage.py runserver 0:"${PORT}"