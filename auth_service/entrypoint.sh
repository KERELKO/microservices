#!/usr/bin/env bash

function init_tables() {
    python3 -c "
from src.db import init_tables
init_tables()
"
    echo "tables initialized"
}

function start_service() {
    python3 -m http.server 8000
}


init_tables
start_service
