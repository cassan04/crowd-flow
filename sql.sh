#!/usr/bin/env bash

set -e

if [ ! -f .env ]; then
    echo "Error: .env file not found."
    exit 1
fi

set -a
source .env
set +a

CONTAINER="postgres_db"
SQL_FILE="./sql/init.sql"

if [ ! -f "$SQL_FILE" ]; then
    echo "Error: SQL script not found at $SQL_FILE"
    exit 1
fi

echo "Executing SQL script on $CONTAINER..."

docker exec -i \
    -e PGPASSWORD="${DB_PASSWORD:-examplepassword}" \
    "$CONTAINER" \
    psql \
        -h "localhost" \
        -U "${DB_USER:-root}" \
        -d "${DB_NAME:-afluencia_db}" \
        -v ON_ERROR_STOP=1 \
    < "$SQL_FILE"

echo "Database update completed successfully."