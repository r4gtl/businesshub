#!/bin/sh

# Aspetta che il DB sia pronto
echo "⏳ Attendo il database su $DB_HOST..."
while ! nc -z $DB_HOST 5432; do
  sleep 1
done
echo "✅ Database disponibile!"

# Applica le migrazioni
echo "📦 Eseguo le migrazioni..."
python manage.py migrate

# Avvia il server Django
echo "🚀 Avvio Django..."
python manage.py runserver 0.0.0.0:8000
