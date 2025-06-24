#!/bin/bash

# Script per avviare Docker in modalità sviluppo o produzione
# Usa: ./up.sh        → modalità sviluppo (.env)
# Usa: ./up.sh prod   → modalità produzione (.env.prod)

# Imposta il file .env in base all'argomento passato
if [ "$1" == "prod" ]; then
    echo "🔧 Avvio in modalità PRODUZIONE"
    ENV_FILE=".env.prod"
else
    echo "🧪 Avvio in modalità SVILUPPO"
    ENV_FILE=".env"
fi

# Verifica se il file esiste
if [ ! -f "$ENV_FILE" ]; then
    echo "❌ File $ENV_FILE non trovato."
    exit 1
fi

# Legge il valore della variabile BACKUP dal file .env
BACKUP_ENABLED=$(grep -E '^BACKUP=' "$ENV_FILE" | cut -d '=' -f2 | tr '[:upper:]' '[:lower:]')
echo $BACKUP_ENABLED
# Imposta i parametri aggiuntivi
if [ "$BACKUP_ENABLED" == "true" ]; then
    echo "📦 Backup ATTIVO"
    PROFILE_OPTION="--profile backup"
else
    echo "📦 Backup DISATTIVO"
    PROFILE_OPTION=""
fi

# Avvia i container
echo "🚀 Eseguo: docker compose --env-file $ENV_FILE up -d --build $PROFILE_OPTION"
docker compose --env-file "$ENV_FILE" up -d --build $PROFILE_OPTION
