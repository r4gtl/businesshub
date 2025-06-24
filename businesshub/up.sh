#!/bin/bash

# Usa: ./up.sh        → sviluppo (.env)
# Usa: ./up.sh prod   → produzione (.env.prod)

# 1. Determina file .env
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

# 3. Leggi variabile BACKUP
BACKUP_ENABLED=$(grep -E '^\s*BACKUP\s*=' "$ENV_FILE" | cut -d '=' -f2 | tr -d '\r' | tr -d ' ' | tr '[:upper:]' '[:lower:]')

chmod +x ./entrypoint_backup.sh

# 4. Avvia i servizi in base a BACKUP
if [ "$BACKUP_ENABLED" == "true" ]; then
    echo "📦 Backup ATTIVO → Avvio tutti i servizi"
    docker compose --env-file "$ENV_FILE" up -d --build
else
    echo "📦 Backup DISATTIVO → Avvio solo web, db, nginx"
    docker compose --env-file "$ENV_FILE" up -d --build web db nginx
fi
