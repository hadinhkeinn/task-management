#!/usr/bin/env bash
# redeploy.sh
# Script to redeploy the API and run migrations without bringing down the database.

echo "Rebuilding and restarting API and Migrate services..."

# We build and start mapping only the api and migrate, leaving db alone!
docker compose build api migrate
docker compose up -d --no-deps --build migrate
docker compose up -d --no-deps --build api

echo "Redeploy complete!"

