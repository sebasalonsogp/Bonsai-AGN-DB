#!/bin/bash
# Wrapper script for additional initialization

set -e

echo "Starting database initialization helper..."

sleep 10

echo "Checking if database tables exist..."
TABLE_COUNT=$(mysql -h localhost -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" -e "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = '$MYSQL_DATABASE' AND table_name IN ('source_agn');" -sN || echo "0")

if [ "$TABLE_COUNT" -lt "1" ]; then
    echo "Tables not found. Creating schema..."
    mysql -h localhost -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" < /docker-entrypoint-initdb.d/01_schema.sql
    
    echo "Loading sample data..."
    mysql -h localhost -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" < /docker-entrypoint-initdb.d/02_sample_data.sql
    
    echo "Schema and sample data loaded successfully!"
else
    echo "Tables already exist, skipping schema and sample data creation."
fi

# Generate larger dataset if requested
if [ "${GENERATE_LARGE_DATASET}" = "true" ]; then
    echo "Generating larger dataset..."
    cd /docker-entrypoint-initdb.d/
    python3 03_generate_data.py
else
    echo "Skipping large dataset generation. Set GENERATE_LARGE_DATASET=true to enable."
fi

echo "Database initialization helper complete!" 