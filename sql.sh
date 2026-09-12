#!/usr/bin/env bash

set -e

if [ ! -f .env ]; then
    echo "Error: .env file not found."
    exit 1
fi

set -a
source .env
set +a

for var in DB_NAME DB_USER DB_PASSWORD; do
    if [ -z "${!var}" ]; then
        echo "Error: $var is not defined in .env"
        exit 1
    fi
done

CONTAINER="postgres_db"
SQL_FILE="./backend/sql/init.sql"

if [ ! -f "$SQL_FILE" ]; then
    echo "Error: SQL script not found at $SQL_FILE"
    exit 1
fi

echo "Executing SQL script on $CONTAINER..."

docker exec -i \
    -e PGPASSWORD="$DB_PASSWORD" \
    "$CONTAINER" \
    psql \
        -h "localhost" \
        -U "$DB_USER" \
        -d "$DB_NAME" \
        -v ON_ERROR_STOP=1 \
    < "$SQL_FILE"

echo "Database update completed successfully."