#!/usr/bin/env bash
# deploy.sh

echo "Pulling latest images..."
docker compose pull api

echo "Starting services ( migrations will run automatically on API startup )..."
docker compose up -d

echo "Redeploy complete!"
docker compose ps