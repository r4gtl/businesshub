#!/bin/bash

echo "🔐 Imposto permessi permanenti su /backup"

# Solo se il mount è vuoto o non ancora sistemato
if [ "$(stat -c %U /backup)" != "stefano" ]; then
  echo "➡️  Forzo proprietà e permessi su /backup"
  chown -R 1000:1000 /backup || true
  chmod -R 777 /backup || true
fi

# umask per i file futuri
umask 000

echo "🚀 Avvio processo di backup..."
exec /init.sh "$@"
