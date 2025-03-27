#!/bin/bash

# Script per visualizzare lo stato dei container Docker
# Usa: ./status.sh          → mostra stato in sviluppo
# Usa: ./status.sh prod     → mostra stato in produzione

if [ "$1" == "prod" ]; then
    echo "📊 Stato ambiente di PRODUZIONE"
    ENV_FILE=".env.prod"
else
    echo "📊 Stato ambiente di SVILUPPO"
    ENV_FILE=".env"
fi

if [ ! -f "$ENV_FILE" ]; then
    echo "❌ File $ENV_FILE non trovato."
    exit 1
fi

# Mostra i container attivi
docker compose --env-file $ENV_FILE ps

# Mostra le ultime righe di log (facoltativo)
echo ""
read -p "Vuoi vedere i log recenti del servizio web? (y/n): " answer
if [[ "$answer" == "y" || "$answer" == "Y" ]]; then
    docker compose --env-file $ENV_FILE logs --tail=20 web
fi
