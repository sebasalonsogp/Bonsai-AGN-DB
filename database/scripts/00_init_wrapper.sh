#!/bin/bash
# Wrapper script for additional initialization

set -e

echo "Starting database initialization helper..."

# Generate larger dataset if requested
if [ "${GENERATE_LARGE_DATASET}" = "true" ]; then
    echo "Generating larger dataset..."
    cd /docker-entrypoint-initdb.d/
    python3 03_generate_data.py
else
    echo "Skipping large dataset generation. Set GENERATE_LARGE_DATASET=true to enable."
fi

echo "Database initialization helper complete!" 