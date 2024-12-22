#!/usr/bin/env bash

set -e

source venv/bin/activate

cd server
echo "Starting server on port $PORT"
socat TCP-LISTEN:$PORT,reuseaddr,fork EXEC:"python3 -u app.py"