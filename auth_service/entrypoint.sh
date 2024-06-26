#!/usr/bin/env bash

function init_tables() {
    python3 -c "
from src.storages.db import init_tables
init_tables()
"
    echo "tables initialized"
}

function start_service() {
    echo "Starting FastAPI application..."
    uvicorn src.entry_points.fastapi.main:app_factory --factory --reload --port 8000 --host 0.0.0.0
}


init_tables
start_service
