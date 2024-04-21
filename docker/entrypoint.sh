#!/bin/bash
set -e

echo "Waiting for services"
python3 /opt/wait_for_services.py

exec "$@"