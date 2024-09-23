# use if need to establish communication between microservices through a message broker
# docker compose -f message_broker/docker-compose.yaml up -d

docker compose -f auth_service/docker-compose.yaml up -d
docker compose -f product_service/docker-compose.yaml up -d
