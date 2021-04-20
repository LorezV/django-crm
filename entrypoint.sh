#!/bin/sh

if [ "$DATABASE" = "postgres" ]; then
  echo "Waiting for postgres..."
  while ! nc -z $SQL_HOST $SQL_PORT; do
    sleep 0.1
  done
  echo "PostgreSQL started"
fi

poetry run python manage.py makemigrations && python manage.py migrate && python manage.py collectstatic --no-input

poetry run gunicorn crm.wsgi:application --reload --log-level debug --capture-output --bind=0.0.0.0

exec "$@"
