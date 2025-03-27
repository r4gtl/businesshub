#!/bin/bash

# Script per fermare Docker in sviluppo o produzione
# Usa: ./down.sh         → stop dev (mantiene volumi)
# Usa: ./down.sh dev -v  → stop dev + elimina volumi
# Usa: ./down.sh prod    → stop prod (non tocca pgdata!)

if [ "$1" == "prod" ]; then
    echo "🛑 Fermando ambiente di PRODUZIONE..."
    ENV_FILE=".env.prod"
    VOLUME_FLAG=""
else
    echo "🛑 Fermando ambiente di SVILUPPO..."
    ENV_FILE=".env"
    VOLUME_FLAG=$2
fi

if [ ! -f "$ENV_FILE" ]; then
    echo "❌ File $ENV_FILE non trovato."
    exit 1
fi

echo "📦 Arresto container con: docker compose --env-file $ENV_FILE down $VOLUME_FLAG"
docker compose --env-file $ENV_FILE down $VOLUME_FLAG
