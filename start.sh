#!/bin/sh
PORT=${PORT:-10000}
uvicorn app.main:app --host 0.0.0.0 --port $PORT
