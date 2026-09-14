#!/usr/bin/env bash

set -e

set -a
source .env
set +a

for var in DB_NAME DB_USER DB_PASSWORD; do
    if [ -z "${!var}" ]; then
        echo "Error: $var is not defined in .env"
        exit 1
    fi
done

echo "Executing backend/sql/init.sql on postgres_db..."

docker exec -i -e PGPASSWORD="$DB_PASSWORD" postgres_db \
    psql -h localhost -U "$DB_USER" -d "$DB_NAME" -v ON_ERROR_STOP=1 \
    < ./backend/sql/init.sql

echo "Database update completed successfully."
