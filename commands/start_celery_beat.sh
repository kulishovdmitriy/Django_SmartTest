#!/bin/bash

rm -f /tmp/celerybeat-schedule /tmp/celerybeat.pid

celery -A app beat -l info --schedule=/tmp/celerybeat-schedule --pidfile=/tmp/celerybeat.pid