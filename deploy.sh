#!/usr/bin/env bash
# deploy.sh

echo "Pulling latest images..."
docker compose pull api migrate

echo "Running migrations..."
docker compose up -d --no-deps migrate
# Chờ migrate xong
docker compose wait migrate

echo "Restarting API..."
docker compose up -d --no-deps api

echo "Redeploy complete!"
docker compose ps