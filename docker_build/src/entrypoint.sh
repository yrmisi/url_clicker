#!/bin/sh
set -e  # Остановить при ошибке

echo "▶️ Running database migrations..."
/app/.venv/bin/alembic upgrade head

echo "✅ Migrations completed. Starting application..."
# exec передаёт сигналы (Ctrl+C) напрямую приложению
exec "$@"
