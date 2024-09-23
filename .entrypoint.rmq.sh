#!/bin/bash

echo "Starting RabbitMQ service..."
docker compose -f message_broker/docker-compose.yaml up -d

echo "Waiting for RabbitMQ to be fully up and running..."
sleep 30

echo "Starting auth_service..."
docker compose -f auth_service/docker-compose.yaml up -d

echo "Starting product_service..."
docker compose -f product_service/docker-compose.yaml up -d
