#!/usr/bin/env bash

function init_tables() {
    echo "------ Starting initalizing of the tables -----"
    python3 -c "
from src.storages.db import init_tables
init_tables()
"
    echo "------ Tables initialized -----"
}

function start_api_service() {
    echo "------Starting FastAPI application-------"
    uvicorn src.entry_points.fastapi.main:app_factory --factory --reload --port 8000 --host 0.0.0.0
}

function start_rmq_service {
    echo "------Connecting to RabbitMQ------"
    python3 -c "
from src.entry_points.rmq import start_service
start_service()
"
}


init_tables
# start_api_service
start_rmq_service
