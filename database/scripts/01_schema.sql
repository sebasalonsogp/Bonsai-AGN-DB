-- Use the created database
USE agndb;

-- Create the source_agn table
CREATE TABLE IF NOT EXISTS source_agn (
    agn_id INT AUTO_INCREMENT PRIMARY KEY,
    ra DOUBLE NOT NULL COMMENT 'Right ascension in degrees',
    declination DOUBLE NOT NULL COMMENT 'Declination in degrees',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_ra (ra),
    INDEX idx_declination (declination)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create the photometry table
CREATE TABLE IF NOT EXISTS photometry (
    phot_id INT AUTO_INCREMENT PRIMARY KEY,
    agn_id INT NOT NULL,
    band_label VARCHAR(50) NOT NULL COMMENT 'Photometric band label',
    filter_name VARCHAR(100) NOT NULL COMMENT 'Filter name',
    mag_value DOUBLE COMMENT 'Magnitude value',
    mag_error DOUBLE COMMENT 'Magnitude error',
    extinction DOUBLE COMMENT 'Extinction value',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (agn_id) REFERENCES source_agn(agn_id) ON DELETE CASCADE,
    INDEX idx_agn_id (agn_id),
    INDEX idx_band_filter (band_label, filter_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create the redshift_measurement table
CREATE TABLE IF NOT EXISTS redshift_measurement (
    redshift_id INT AUTO_INCREMENT PRIMARY KEY,
    agn_id INT NOT NULL,
    redshift_type VARCHAR(50) NOT NULL COMMENT 'Type of redshift measurement',
    z_value DOUBLE NOT NULL COMMENT 'Redshift value',
    z_error DOUBLE COMMENT 'Redshift error',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (agn_id) REFERENCES source_agn(agn_id) ON DELETE CASCADE,
    INDEX idx_agn_id (agn_id),
    INDEX idx_z_value (z_value)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create the classification table
CREATE TABLE IF NOT EXISTS classification (
    class_id INT AUTO_INCREMENT PRIMARY KEY,
    agn_id INT NOT NULL,
    spec_class VARCHAR(50) COMMENT 'Spectroscopic classification',
    gen_class VARCHAR(50) COMMENT 'General classification',
    xray_class VARCHAR(50) COMMENT 'X-ray classification',
    best_class VARCHAR(50) COMMENT 'Best available classification',
    image_class VARCHAR(50) COMMENT 'Image-based classification',
    sed_class VARCHAR(50) COMMENT 'Spectral energy distribution classification',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (agn_id) REFERENCES source_agn(agn_id) ON DELETE CASCADE,
    INDEX idx_agn_id (agn_id),
    INDEX idx_best_class (best_class)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci; 