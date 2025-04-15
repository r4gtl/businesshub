#!/bin/bash

# Usa: ./up.sh        → sviluppo (.env)
# Usa: ./up.sh prod   → produzione (.env.prod)

# 1. Determina il file .env
if [ "$1" == "prod" ]; then
    echo "🔧 Avvio in modalità PRODUZIONE"
    ENV_FILE=".env.prod"
else
    echo "🧪 Avvio in modalità SVILUPPO"
    ENV_FILE=".env"
fi

# 2. Controlla esistenza file
if [ ! -f "$ENV_FILE" ]; then
    echo "❌ File $ENV_FILE non trovato."
    exit 1
fi

# 3. Leggi BACKUP dal file, ignora commenti, rimuovi spazi e \r
BACKUP_ENABLED=$(grep -E '^\s*BACKUP\s*=' "$ENV_FILE" | cut -d '=' -f2 | tr -d '\r' | tr -d ' ' | tr '[:upper:]' '[:lower:]')

# 4. Imposta profilo opzionale
if [ "$BACKUP_ENABLED" == "true" ]; then
    echo "📦 Backup ATTIVO"
    PROFILE_OPTION="--profile backup"
else
    echo "📦 Backup DISATTIVO"
    PROFILE_OPTION=""
fi

# 5. Avvia docker compose
# echo "🚀 Eseguo: docker compose --env-file $ENV_FILE up -d --build $PROFILE_OPTION"
# docker compose --env-file "$ENV_FILE" up -d --build $PROFILE_OPTION
echo "👉 Sto usando Docker Compose da: $(which docker)"
docker compose version
docker compose --env-file "$ENV_FILE" up -d --build $PROFILE_OPTION