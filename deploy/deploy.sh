#!/bin/sh

set -e

echo "Starting anonymous chat production deployment"

docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml build
docker compose -f docker-compose.prod.yml up -d

echo "Deployment finished"
