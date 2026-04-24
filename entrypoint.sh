#!/bin/sh
set -e

# Run datatabase migrations
echo "Running database migrations..."
alembic upgrade head

# Start the application
echo "Starting application..."
exec "$@"
