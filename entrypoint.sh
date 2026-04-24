#!/bin/sh

set -e

alembic upgrade head

exec uvicorn orders_service.api.main:app \
    --host 0.0.0.0 \
    --port 8000
