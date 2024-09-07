#!/usr/bin/env bash

function init_tables() {
    echo "Starting to initialize SQL tables..."
    python3 -c "
from src.common.db.sqlalchemy.config import init_tables
init_tables()
"
    echo "==== SQL Tables initialized ===="
}

function start_api_service() {
    echo "Starting FastAPI application..."
    uvicorn src.entrypoints.fastapi_app:app_factory --factory --reload --port 8001 --host 0.0.0.0
}

function start_rmq_service {
    echo "Connecting to RabbitMQ..."
    python3 -c "
from src.entrypoints.rabbitmq_consumer import main
main()
"
}

function start_grpc_service {
    echo "Run gRPC service..."
    python3 -c "
from src.entrypoints.grpc_server import main
main()
"
}


init_tables &
start_api_service &
# start_rmq_service &
start_grpc_service & 
wait
