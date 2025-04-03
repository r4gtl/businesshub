#!/bin/sh

export DJANGO_SETTINGS_MODULE=businesshub.settings

# Aspetta che il DB sia pronto
echo "⏳ Attendo il database su $DB_HOST..."
while ! nc -z $DB_HOST 5432; do
  sleep 1
done
echo "✅ Database disponibile!"

set -e

echo "🔄 Creando migrazioni..."
# Crea le migrazioni se ci sono modifiche ai modelli
python manage.py makemigrations

echo "🔄 Applying database migrations..."
python manage.py migrate

DEBUG_MODE=$(python -c "from django.conf import settings; print(settings.DEBUG)")

if [ "$DEBUG_MODE" = "False" ]; then
  echo "📦 Collecting static files (production only)..."
  python manage.py collectstatic --noinput

  echo "🚀 Starting Gunicorn server..."
  exec gunicorn businesshub.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120
else
  echo "⚙️  DEBUG mode: starting Django development server..."
  exec python manage.py runserver 0.0.0.0:8000
fi