#!/bin/sh
set -e

until pg_isready -h db -p 5432 -U books_user; do
  echo "Waiting for postgres..."
  sleep 2
done

echo "Postgres is ready, running migrations..."
alembic upgrade head

echo "Starting app..."
exec "$@"