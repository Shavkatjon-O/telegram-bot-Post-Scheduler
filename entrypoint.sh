#!/bin/sh

# run migrations
python manage.py migrate
exec "$@"
