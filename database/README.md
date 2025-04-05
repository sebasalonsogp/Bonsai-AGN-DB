# AGN-DB Database

This directory contains the MariaDB database setup for the AGN-DB project.

## Overview

The database follows the schema defined in the ERD diagram and includes the following tables:

- `source_agn`: Contains the main AGN sources with RA/DEC coordinates
- `photometry`: Stores photometric measurements for each source
- `redshift_measurement`: Contains redshift measurements for sources
- `classification`: Stores various classification information for sources

## Usage

### Docker Setup

1. Build the Docker image:
   ```
   docker build -t agndb-database .
   ```

2. Run the container:
   ```
   docker run -d \
     --name agndb-db \
     -p 3306:3306 \
     -e MYSQL_ROOT_PASSWORD=root_password \
     -e MYSQL_DATABASE=agndb \
     -e MYSQL_USER=agndb_user \
     -e MYSQL_PASSWORD=agndb_password \
     -e GENERATE_LARGE_DATASET=false \
     agndb-database
   ```

   Set `GENERATE_LARGE_DATASET=true` to generate a larger dataset (~5000 sources with related data).

### Connecting to the Database

From the host:
```
mysql -h 127.0.0.1 -P 3306 -u agndb_user -pagndb_password agndb
```

From the backend application, use the following connection string:
```
mariadb+asyncmy://agndb_user:agndb_password@localhost:3306/agndb
```

## Data Generation

The database includes:

1. **Basic Sample Data**: Always loaded, contains 100 source AGNs with related measurements
2. **Extended Dataset**: Optionally generated, adds ~5000 additional sources

### Manual Data Generation

To manually run the data generation script:

```
# Connect to the container
docker exec -it agndb-db bash

# Run the script
cd /docker-entrypoint-initdb.d
python3 03_generate_data.py
```

## Database Schema

### source_agn
- `agn_id`: Primary key
- `ra`: Right ascension in degrees
- `dec`: Declination in degrees
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### photometry
- `phot_id`: Primary key
- `agn_id`: Foreign key to source_agn
- `band_label`: Photometric band label
- `filter_name`: Filter name
- `mag_value`: Magnitude value
- `mag_error`: Magnitude error
- `extinction`: Extinction value
- `created_at`, `updated_at`: Timestamps

### redshift_measurement
- `redshift_id`: Primary key
- `agn_id`: Foreign key to source_agn
- `redshift_type`: Type of redshift measurement
- `z_value`: Redshift value
- `z_error`: Redshift error
- `created_at`, `updated_at`: Timestamps

### classification
- `class_id`: Primary key
- `agn_id`: Foreign key to source_agn
- `spec_class`: Spectroscopic classification
- `gen_class`: General classification
- `xray_class`: X-ray classification
- `best_class`: Best available classification
- `image_class`: Image-based classification
- `sed_class`: SED classification
- `created_at`, `updated_at`: Timestamps 