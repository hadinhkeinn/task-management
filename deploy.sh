#!/usr/bin/env bash
# deploy.sh

echo "Pulling latest images..."
docker compose pull api migrate

echo "Ensuring database is running..."
docker compose up -d db

echo "Running migrations..."
docker compose up -d migrate
# Chờ migrate xong
docker compose wait migrate

echo "Restarting API..."
docker compose up -d api

echo "Redeploy complete!"
docker compose ps