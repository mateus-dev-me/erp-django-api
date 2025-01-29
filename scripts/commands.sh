#!/bin/sh

set -e

echo "🟡 Aguardando a inicialização do banco de dados Postgres ($DB_HOST:$DB_PORT)..."
until nc -z "$DB_HOST" "$DB_PORT"; do
  sleep 2
done
echo "✅ Banco de dados Postgres iniciado com sucesso ($DB_HOST:$DB_PORT)"

echo "⚙️ Realizando migrações..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "🚀 Iniciando o servidor Gunicorn para o aplicativo Django..."
exec gunicorn core.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 3 
