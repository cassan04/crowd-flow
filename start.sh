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

[ "$NODE_ENV" = "development" ] && MODE="dev" || MODE="prod"

# Block production deployments that still use the example credentials
if [ "$MODE" = "prod" ]; then
    FORBIDDEN_DEFAULTS=(
        "password" "admin" "root" "afluencia_db"
        "examplepassword"
        "jwt_secret_super_seguro_aqui_123_todo_al_rojo"
        "password_super_secreta"
    )

    for val in "$DB_PASSWORD" "$DB_USER" "$DB_NAME" "$JWT_SECRET" "$REFRESH_SECRET"; do
        for forbidden in "${FORBIDDEN_DEFAULTS[@]}"; do
            if [ "$val" = "$forbidden" ]; then
                error_exit "Production deployment blocked. Insecure default value detected in .env: '$val'"
            fi
        done
    done
fi

echo -e "${BLUE}--- CROWD-FLOW APP (${MODE}) ---${NC}"

# The prod profile only matters once the apache service is enabled
PROFILE=()
[ "$MODE" = "prod" ] && PROFILE=(--profile prod)

# Compose waits for the database healthcheck before starting the backend,
# so the schema can be applied as soon as this returns
docker compose "${PROFILE[@]}" up -d --build || error_exit "Docker Compose failed to start."
./sql.sh || error_exit "Database schema initialization failed."

echo -e "\n${GREEN}Environment ready!${NC}"
# echo -e "Frontend:       ${BLUE}localhost:XXXX${NC}"
echo -e "Backend API:    ${BLUE}http://localhost:${API_PORT}${NC}"
echo -e "PostgreSQL:     ${BLUE}localhost:5432${NC}"
echo -e "Kafka Broker:   ${BLUE}localhost:29092${NC}"
echo -e "To see logs:    ${BLUE}docker compose logs -f${NC}"
echo -e "Shut down:      ${BLUE}docker compose down${NC}"
