#!/usr/bin/env bash

GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

error_exit() {
    echo -e "${RED}Error: $1${NC}"
    exit 1
}

if [ ! -f .env ]; then
    error_exit ".env file not found. Copy .env.example to .env and fill it in."
fi

set -a
source .env
set +a

# The containers run the node_modules installed here on the host
for dir in backend frontend; do
    if [ ! -d "$dir/node_modules" ]; then
        error_exit "$dir/node_modules not found. Run: (cd $dir && npm ci)"
    fi
done

echo -e "${BLUE}--- CROWD-FLOW APP (dev) ---${NC}"

# Compose waits for the database healthcheck before starting the backend,
# so the schema can be applied as soon as this returns.
docker compose up -d --build || error_exit "Docker Compose failed to start."
./sql.sh || error_exit "Database schema initialization failed."

echo -e "\n${GREEN}Environment ready!${NC}"
echo -e "Frontend:       ${BLUE}http://localhost:5173${NC}"
echo -e "Backend API:    ${BLUE}http://localhost:${API_PORT}${NC}"
echo -e "PostgreSQL:     ${BLUE}localhost:5432${NC}"
echo -e "Kafka Broker:   ${BLUE}localhost:29092${NC}"
echo -e "To see logs:    ${BLUE}docker compose logs -f${NC}"
echo -e "Shut down:      ${BLUE}docker compose down${NC}"
