#!/bin/bash

# CONFIG
REPO_URL="git@github.com:r4gtl/businesshub.git"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PGDATA_DIR="$PROJECT_DIR/pgdata"

# Ambiente: se non specificato, usa dev
if [ "$1" == "prod" ]; then
    ENV_MODE="prod"
    ENV_FILE=".env.prod"
else
    ENV_MODE="dev"
    ENV_FILE=".env"
fi

echo "🛠 Setup ambiente di ${ENV_MODE^^}"

# 1. Clona o aggiorna repo
if [ -d "$PROJECT_DIR/.git" ]; then
    echo "📦 Repository già presente, aggiorno..."
    cd "$PROJECT_DIR" && git pull
else
    echo "📥 Clono il repository..."
    git clone "$REPO_URL" "$PROJECT_DIR"
fi

cd "$PROJECT_DIR" || exit 1

# 2. Docker install
if ! command -v docker &> /dev/null; then
    echo "🐳 Docker non trovato, installo..."
    sudo apt update
    sudo apt install -y docker.io
    sudo systemctl enable --now docker
fi

# 3. Docker Compose plugin install
if ! docker compose version &> /dev/null; then
    echo "🧩 Installo Docker Compose V2 (plugin)..."
    sudo apt install -y docker-compose-plugin
fi

# 4. pgdata in produzione
if [ "$ENV_MODE" == "prod" ]; then
    if [ ! -d "$PGDATA_DIR" ]; then
        echo "📂 Creo pgdata: $PGDATA_DIR"
        mkdir "$PGDATA_DIR"
        sudo chown -R 999:999 "$PGDATA_DIR"
    fi
fi

# 5. Cambia permessi della cartella accounts
echo "🔑 Cambia permessi della cartella accounts"
if [ -d "$ACCOUNTS_DIR" ]; then
    sudo chown -R 1000:1000 "$ACCOUNTS_DIR"
else
    echo "🚨 La cartella 'accounts' non esiste!"
fi

# 6. Script eseguibili
chmod +x up.sh down.sh status.sh

# 7. Avvia in base all'ambiente
echo "🚀 Avvio docker con ./up.sh $ENV_MODE"
./up.sh "$ENV_MODE"