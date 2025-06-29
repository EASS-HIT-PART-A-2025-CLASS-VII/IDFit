#!/bin/sh

echo "🕒 Waiting for Mongo ..."
until nc -z idfit-mongo 27017; do
  sleep 1
done

echo "✅ Mongo is avtivated, sending roles..."
python init_roles.py || echo "⚠️ לא הצליח לטעון תפקידים, ממשיך..."

echo "🚀 FastAPI is On"
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
