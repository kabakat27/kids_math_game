#!/usr/bin/env bash
set -euo pipefail

if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
  COMPOSE=(docker compose)
elif command -v docker-compose >/dev/null 2>&1; then
  COMPOSE=(docker-compose)
else
  echo "Error: Docker Compose is not available. Install Docker Desktop or docker-compose." >&2
  exit 1
fi

echo "Using: ${COMPOSE[*]}"
echo "Building containers..."
"${COMPOSE[@]}" build

echo "Build complete."
