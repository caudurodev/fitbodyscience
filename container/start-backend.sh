#!/usr/bin/env bash

# load .env variables
if [ -f .env ]; then
  # Load the .env file
  set -o allexport
  source .env
  set +o allexport
else
  echo ".env file not found. Make sure it exists in the same directory as this script."
  exit 1
fi

NHOST_NETWORK_NAME=${NHOST_NETWORK_NAME} docker compose -p ${PROJECT_NAME} -f docker-compose.override.yml up --no-deps
