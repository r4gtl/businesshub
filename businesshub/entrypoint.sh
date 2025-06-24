#!/bin/sh

export DJANGO_SETTINGS_MODULE=businesshub.settings

# Aspetta che il DB sia pronto
echo "⏳ Attendo che PostgreSQL sia pronto su $DB_HOST..."
until pg_isready -h "$DB_HOST" -p 5432 -U "$POSTGRES_USER"; do
  >&2 echo "🕓 Database non ancora pronto - attendo..."
  sleep 2
done
echo "✅ Database disponibile!"


set -e

echo "🔄 Creando migrazioni..."
# Crea le migrazioni se ci sono modifiche ai modelli
python3 manage.py makemigrations


echo "🔄 Applying database migrations..."
python3 manage.py migrate

DEBUG_MODE=$(python3 -c "from django.conf import settings; print(settings.DEBUG)")

if [ "$DEBUG_MODE" = "False" ]; then
  echo "📦 Collecting static files (production only)..."
  python3 manage.py collectstatic --noinput

  echo "🚀 Starting Gunicorn server..."
  exec gunicorn businesshub.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120
else
  echo "⚙️  DEBUG mode: starting Django development server..."
  exec python3 manage.py runserver 0.0.0.0:8000
fi
