#!/bin/bash

set -e

echo "🛠️ Fix Docker Compose con supporto a --profile"

# 1. Elimina versioni errate/plugin se presenti
echo "🔍 Rimozione eventuali versioni di docker-compose legacy..."

sudo rm -f /usr/local/bin/docker-compose
sudo rm -f /usr/bin/docker-compose
sudo rm -f /usr/libexec/docker/cli-plugins/docker-compose || true

# 2. Crea cartella plugin se non esiste
echo "📂 Creo cartella ~/.docker/cli-plugins se non esiste..."
mkdir -p ~/.docker/cli-plugins

# 3. Scarica e installa compose standalone (v2.24.5)
echo "⬇️ Scarico docker-compose standalone..."
curl -SL https://github.com/docker/compose/releases/download/v2.24.5/docker-compose-linux-x86_64 \
    -o ~/.docker/cli-plugins/docker-compose

chmod +x ~/.docker/cli-plugins/docker-compose

# 4. Verifica versione e supporto profili
echo "✅ Verifica installazione..."
docker compose version

echo -n "🔎 Verifica supporto --profile... "
if docker compose ls --help | grep -q -- "--profile"; then
    echo "OK ✅"
else
    echo "❌ COMANDO --profile NON supportato. Qualcosa non va."
    exit 1
fi

echo "🎉 Docker Compose con supporto ai profili installato con successo!"
