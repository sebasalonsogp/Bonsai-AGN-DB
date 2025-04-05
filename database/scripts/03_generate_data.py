#!/usr/bin/env python3
"""
Data generation script for AGN-DB.
This script generates a large amount of synthetic data for testing purposes.
Run this after the database schema has been created.
"""
import random
import math
import pymysql
import time
from datetime import datetime

# Database connection parameters
DB_CONFIG = {
    'host': 'localhost',
    'user': 'agndb_user',
    'password': 'agndb_password',
    'database': 'agndb',
}

# Constants for data generation
NUM_SOURCES = 5000  # Adjust as needed
PHOTOMETRY_PER_SOURCE_MIN = 3
PHOTOMETRY_PER_SOURCE_MAX = 10
REDSHIFT_PROBABILITY = 0.7  # Probability a source has redshift
CLASSIFICATION_PROBABILITY = 0.8  # Probability a source has classification

# Possible values for classifications
SPEC_CLASSES = ['BLAGN', 'NLAGN', None]
GEN_CLASSES = ['Seyfert 1', 'Seyfert 1.5', 'Seyfert 2', 'Quasar', 'LINER', 'AGN Candidate', None]
XRAY_CLASSES = ['Type 1', 'Type 2', None]
BEST_CLASSES = ['Seyfert 1', 'Seyfert 1.5', 'Seyfert 2', 'Quasar', 'LINER', 'AGN Candidate']
IMAGE_CLASSES = ['Point Source', 'Extended', None]
SED_CLASSES = ['Blue Continuum', 'Red Continuum', 'Flat Continuum', None]

# Photometry bands and filters
PHOTOMETRY_BANDS = {
    'U': ['SDSS u', 'Johnson U'],
    'B': ['SDSS g', 'Johnson B'],
    'V': ['SDSS r', 'Johnson V'],
    'R': ['SDSS i', 'Johnson R'],
    'I': ['SDSS z', 'Johnson I'],
    'J': ['2MASS J'],
    'H': ['2MASS H'],
    'K': ['2MASS K', '2MASS Ks']
}

# Redshift types
REDSHIFT_TYPES = ['spectroscopic', 'photometric']


def generate_ra():
    """Generate a random right ascension value (0-360 degrees)."""
    return random.uniform(0, 360)


def generate_dec():
    """Generate a random declination value (-90 to +90 degrees)."""
    return random.uniform(-90.0, 90.0)


def generate_photometry(source_id, conn):
    """Generate photometry entries for a source."""
    cursor = conn.cursor()
    
    # Randomly select number of photometry entries
    num_entries = random.randint(PHOTOMETRY_PER_SOURCE_MIN, PHOTOMETRY_PER_SOURCE_MAX)
    
    # Randomly select distinct bands to use
    bands = random.sample(list(PHOTOMETRY_BANDS.keys()), min(num_entries, len(PHOTOMETRY_BANDS)))
    
    for band in bands:
        # For each band, select a filter
        filter_name = random.choice(PHOTOMETRY_BANDS[band])
        
        # Generate magnitude value based on band (rough simulation)
        if band in ['U', 'B']:
            mag_value = random.uniform(18, 22)  # Fainter in blue
        elif band in ['V', 'R', 'I']:
            mag_value = random.uniform(17, 21)  # Mid-range
        else:  # Infrared
            mag_value = random.uniform(15, 19)  # Brighter in IR
            
        # Error increases with magnitude
        mag_error = 0.01 + (mag_value - 15) * 0.005
        
        # Extinction decreases with wavelength
        if band in ['U', 'B']:
            extinction = random.uniform(0.05, 0.2)
        elif band in ['V', 'R', 'I']:
            extinction = random.uniform(0.02, 0.1)
        else:  # Infrared
            extinction = random.uniform(0, 0.03)
            
        # Insert into database
        cursor.execute("""
            INSERT INTO photometry 
            (agn_id, band_label, filter_name, mag_value, mag_error, extinction)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (source_id, band, filter_name, mag_value, mag_error, extinction))
    
    cursor.close()


def generate_redshift(source_id, conn):
    """Generate a redshift measurement for a source."""
    if random.random() > REDSHIFT_PROBABILITY:
        return  # Skip redshift for some sources
        
    cursor = conn.cursor()
    
    # Choose redshift type with bias toward spectroscopic
    redshift_type = random.choices(
        REDSHIFT_TYPES, 
        weights=[0.6, 0.4],  # 60% spectroscopic, 40% photometric
        k=1
    )[0]
    
    # Generate redshift value with realistic distribution
    # Use a log-normal-ish distribution peaking around z=0.5
    z_value = random.lognormvariate(mu=-1, sigma=1)
    # Clip to realistic range
    z_value = min(max(z_value, 0.02), 3.0)
    
    # Error depends on type
    if redshift_type == 'spectroscopic':
        z_error = z_value * random.uniform(0.001, 0.01)
    else:
        z_error = z_value * random.uniform(0.05, 0.15)
        
    # Insert into database
    cursor.execute("""
        INSERT INTO redshift_measurement 
        (agn_id, redshift_type, z_value, z_error)
        VALUES (%s, %s, %s, %s)
    """, (source_id, redshift_type, z_value, z_error))
    
    cursor.close()


def generate_classification(source_id, conn):
    """Generate a classification for a source."""
    if random.random() > CLASSIFICATION_PROBABILITY:
        return  # Skip classification for some sources
        
    cursor = conn.cursor()
    
    # Generate consistent classifications
    is_type1 = random.random() > 0.5  # Type 1 or Type 2 AGN
    
    if is_type1:
        spec_class = 'BLAGN' if random.random() > 0.1 else None  # 90% have spec class if Type 1
        gen_class = random.choice(['Seyfert 1', 'Seyfert 1.5', 'Quasar'])
        xray_class = 'Type 1'
        best_class = gen_class
        image_class = 'Point Source' if random.random() > 0.2 else 'Extended'
        sed_class = 'Blue Continuum' if random.random() > 0.3 else random.choice(['Red Continuum', 'Flat Continuum'])
    else:
        spec_class = 'NLAGN' if random.random() > 0.3 else None  # 70% have spec class if Type 2
        gen_class = random.choice(['Seyfert 2', 'LINER']) if random.random() > 0.3 else 'AGN Candidate'
        xray_class = 'Type 2'
        best_class = gen_class
        image_class = 'Extended' if random.random() > 0.1 else 'Point Source'
        sed_class = 'Red Continuum' if random.random() > 0.3 else random.choice(['Blue Continuum', 'Flat Continuum'])
    
    # Insert into database
    cursor.execute("""
        INSERT INTO classification 
        (agn_id, spec_class, gen_class, xray_class, best_class, image_class, sed_class)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (source_id, spec_class, gen_class, xray_class, best_class, image_class, sed_class))
    
    cursor.close()


def populate_source_agn(cursor, count=5000):
    """Populate source_agn table with random data."""
    print(f"Generating {count} sources...")
    for _ in range(count):
        ra = generate_ra()
        dec = generate_dec()
        cursor.execute(
            "INSERT IGNORE INTO source_agn (ra, declination) VALUES (%s, %s)",
            (ra, dec)
        )


def main():
    """Main function to generate data."""
    print(f"Generating {NUM_SOURCES} sources with associated data...")
    start_time = time.time()
    
    # Connect to database
    conn = pymysql.connect(**DB_CONFIG)
    conn.autocommit(False)
    
    try:
        cursor = conn.cursor()
        
        # Check if database already has data
        cursor.execute("SELECT COUNT(*) FROM source_agn")
        existing_count = cursor.fetchone()[0]
        
        if existing_count > 0:
            confirm = input(f"Database already has {existing_count} sources. Continue? (y/n): ")
            if confirm.lower() != 'y':
                print("Aborting.")
                return
        
        # Generate sources in batches for efficiency
        batch_size = 100
        for batch_start in range(101, NUM_SOURCES + 101, batch_size):  # Start from 101 to avoid conflicts with sample data
            # Generate a batch of sources
            for i in range(batch_start, min(batch_start + batch_size, NUM_SOURCES + 101)):
                # Create source
                ra = generate_ra()
                dec = generate_dec()
                cursor.execute(
                    "INSERT IGNORE INTO source_agn (ra, declination) VALUES (%s, %s)",
                    (ra, dec)
                )
                source_id = cursor.lastrowid
                
                # Generate related data
                generate_photometry(source_id, conn)
                generate_redshift(source_id, conn)
                generate_classification(source_id, conn)
            
            # Commit batch
            conn.commit()
            
            # Progress update
            progress = min(100, (batch_start - 101 + batch_size) / NUM_SOURCES * 100)
            elapsed = time.time() - start_time
            print(f"Progress: {progress:.1f}% ({min(batch_start + batch_size - 101, NUM_SOURCES)} / {NUM_SOURCES}), "
                  f"Time elapsed: {elapsed:.1f}s")
    
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        conn.close()
    
    total_time = time.time() - start_time
    print(f"Data generation complete. Total time: {total_time:.1f}s")


if __name__ == "__main__":
    main() 