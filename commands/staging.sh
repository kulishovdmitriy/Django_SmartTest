#!/bin/bash

echo "Waiting for PostgreSQL to be ready..."

sleep 5

echo "Running Django with ALLOWED_HOSTS: $ALLOWED_HOSTS"
echo "Using Gunicorn with $WORKERS workers on port $PORT"

gunicorn -w ${WORKERS} -b 0.0.0.0:"${PORT}" app.wsgi:application