#!/bin/bash

# CONFIGURA QUESTE VARIABILI IN BASE AL TUO PROGETTO
REPO_URL="git@github.com:r4gtl/businesshub.git"
PROJECT_DIR="/home/stefano/businesshub"
PGDATA_DIR="$PROJECT_DIR/pgdata"

echo "🛠 Setup ambiente di PRODUZIONE"

# 1. Clona o aggiorna il repository
if [ -d "$PROJECT_DIR/.git" ]; then
    echo "📦 Repository già presente, aggiorno..."
    cd "$PROJECT_DIR" && git pull
else
    echo "📥 Clono il repository..."
    git clone "$REPO_URL" "$PROJECT_DIR"
fi

cd "$PROJECT_DIR" || exit 1

# 2. Controllo/installazione Docker
if ! command -v docker &> /dev/null; then
    echo "🐳 Docker non installato, installo..."
    sudo apt update
    sudo apt install -y docker.io
    sudo systemctl start docker
    sudo systemctl enable docker
fi

# 3. Controllo/installazione Docker Compose
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "🔧 Installo Docker Compose..."
    sudo apt install -y docker-compose
fi

# 4. Crea pgdata se non esiste
if [ ! -d "$PGDATA_DIR" ]; then
    echo "📂 Creo la cartella per i dati del database: $PGDATA_DIR"
    mkdir "$PGDATA_DIR"
    sudo chown -R 999:999 "$PGDATA_DIR"
fi

# 5. Rendo eseguibili gli script .sh
chmod +x up.sh down.sh status.sh

# 6. Avvio il sistema in modalità produzione
./up.sh prod
