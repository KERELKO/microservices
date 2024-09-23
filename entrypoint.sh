echo "run services..."
docker compose -f auth_service/docker-compose.yaml up -d
docker compose -f product_service/docker-compose.yaml up -d
