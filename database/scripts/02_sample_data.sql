-- Use the created database
USE agndb;

-- Insert sample data into source_agn table (100 sources)
INSERT IGNORE INTO source_agn (ra, declination) VALUES
    (14.2356, -10.5689), -- Source 1
    (45.7891, 23.4567),  -- Source 2
    (120.4567, 45.8932), -- Source 3
    (180.6789, -30.4521), -- Source 4
    (270.1234, 15.7890), -- Source 5
    (300.5678, -25.3456), -- Source 6
    (13.7895, 5.6789),   -- Source 7
    (90.1234, 37.8910),  -- Source 8
    (150.5678, -42.1357), -- Source 9
    (220.8910, 8.9012),  -- Source 10
    (10.1234, -15.4321), -- Source 11
    (50.5678, 20.8765),  -- Source 12
    (100.9012, 40.3456), -- Source 13
    (190.3456, -35.7890), -- Source 14
    (280.7890, 18.2345), -- Source 15
    (310.2345, -28.6789), -- Source 16
    (15.6789, 7.0123),   -- Source 17
    (85.0123, 32.4567),  -- Source 18
    (160.4567, -45.8901), -- Source 19
    (230.8901, 12.3456), -- Source 20
    (22.3456, -8.7654),  -- Source 21
    (55.7654, 25.3210),  -- Source 22
    (110.3210, 48.7654), -- Source 23
    (185.7654, -22.3210), -- Source 24
    (260.3210, 11.7654), -- Source 25
    (320.7654, -33.3210), -- Source 26
    (18.3210, 3.7654),   -- Source 27
    (80.7654, 28.3210),  -- Source 28
    (155.3210, -38.7654), -- Source 29
    (240.7654, 15.3210), -- Source 30
    (30.3210, -5.7654),  -- Source 31
    (60.7654, 35.3210),  -- Source 32
    (105.3210, 55.7654), -- Source 33
    (195.7654, -17.3210), -- Source 34
    (250.3210, 25.7654), -- Source 35
    (330.7654, -20.3210), -- Source 36
    (25.3210, 10.7654),  -- Source 37
    (95.7654, 40.3210),  -- Source 38
    (165.3210, -30.7654), -- Source 39
    (245.7654, 5.3210),  -- Source 40
    (35.3210, -12.7654), -- Source 41
    (65.7654, 42.3210),  -- Source 42
    (115.3210, 60.7654), -- Source 43
    (205.7654, -25.3210), -- Source 44
    (275.3210, 30.7654), -- Source 45
    (340.7654, -15.3210), -- Source 46
    (28.3210, 15.7654),  -- Source 47
    (78.7654, 45.3210),  -- Source 48
    (170.3210, -35.7654), -- Source 49
    (255.7654, 2.3210),  -- Source 50
    (40.3210, -18.7654), -- Source 51
    (70.7654, 38.3210),  -- Source 52
    (125.3210, 50.7654), -- Source 53
    (200.7654, -28.3210), -- Source 54
    (265.3210, 20.7654), -- Source 55
    (345.7654, -10.3210), -- Source 56
    (8.3210, 12.7654),   -- Source 57
    (75.7654, 48.3210),  -- Source 58
    (175.3210, -32.7654), -- Source 59
    (235.7654, 7.3210),  -- Source 60
    (42.3210, -20.7654), -- Source 61
    (72.7654, 32.3210),  -- Source 62
    (130.3210, 52.7654), -- Source 63
    (210.7654, -24.3210), -- Source 64
    (267.3210, 22.7654), -- Source 65
    (347.7654, -8.3210), -- Source 66
    (6.3210, 17.7654),   -- Source 67
    (88.7654, 47.3210),  -- Source 68
    (178.3210, -29.7654), -- Source 69
    (238.7654, 9.3210),  -- Source 70
    (43.3210, -22.7654), -- Source 71
    (73.7654, 29.3210),  -- Source 72
    (133.3210, 53.7654), -- Source 73
    (213.7654, -23.3210), -- Source 74
    (268.3210, 24.7654), -- Source 75
    (348.7654, -6.3210), -- Source 76
    (7.3210, 19.7654),   -- Source 77
    (89.7654, 49.3210),  -- Source 78
    (179.3210, -27.7654), -- Source 79
    (239.7654, 11.3210), -- Source 80
    (44.3210, -24.7654), -- Source 81
    (74.7654, 27.3210),  -- Source 82
    (134.3210, 54.7654), -- Source 83
    (214.7654, -21.3210), -- Source 84
    (269.3210, 26.7654), -- Source 85
    (349.7654, -4.3210), -- Source 86
    (8.3210, 21.7654),   -- Source 87
    (91.7654, 51.3210),  -- Source 88
    (177.3210, -26.7654), -- Source 89
    (237.7654, 13.3210), -- Source 90
    (45.3210, -26.7654), -- Source 91
    (75.7654, 22.3210),  -- Source 92
    (135.3210, 56.7654), -- Source 93
    (215.7654, -19.3210), -- Source 94
    (270.3210, 28.7654), -- Source 95
    (350.7654, -2.3210), -- Source 96
    (9.3210, 23.7654),   -- Source 97
    (92.7654, 53.3210),  -- Source 98
    (176.3210, -24.7654), -- Source 99
    (236.7654, 14.3210); -- Source 100

-- Insert sample data into photometry table (multiple entries per source)
-- Common photometric bands: U, B, V, R, I, J, H, K
INSERT INTO photometry (agn_id, band_label, filter_name, mag_value, mag_error, extinction) VALUES
    -- For Source 1
    (1, 'U', 'SDSS u', 18.23, 0.05, 0.12),
    (1, 'B', 'SDSS g', 17.45, 0.03, 0.09),
    (1, 'V', 'SDSS r', 16.78, 0.02, 0.07),
    (1, 'R', 'SDSS i', 16.34, 0.02, 0.05),
    (1, 'I', 'SDSS z', 16.12, 0.03, 0.04),
    
    -- For Source 2
    (2, 'U', 'SDSS u', 19.56, 0.08, 0.15),
    (2, 'B', 'SDSS g', 18.89, 0.05, 0.11),
    (2, 'V', 'SDSS r', 18.23, 0.04, 0.08),
    (2, 'R', 'SDSS i', 17.91, 0.03, 0.06),
    (2, 'I', 'SDSS z', 17.67, 0.04, 0.05),
    
    -- For Source 3
    (3, 'U', 'SDSS u', 20.12, 0.10, 0.18),
    (3, 'B', 'SDSS g', 19.45, 0.06, 0.14),
    (3, 'V', 'SDSS r', 18.79, 0.05, 0.10),
    (3, 'R', 'SDSS i', 18.32, 0.04, 0.08),
    (3, 'I', 'SDSS z', 18.05, 0.05, 0.06),
    
    -- For Source 4
    (4, 'J', '2MASS J', 16.54, 0.03, 0.02),
    (4, 'H', '2MASS H', 16.21, 0.02, 0.01),
    (4, 'K', '2MASS K', 15.98, 0.02, 0.01),
    
    -- For Source 5
    (5, 'U', 'SDSS u', 17.45, 0.04, 0.11),
    (5, 'B', 'SDSS g', 16.78, 0.02, 0.08),
    (5, 'V', 'SDSS r', 16.23, 0.02, 0.06),
    (5, 'R', 'SDSS i', 15.89, 0.02, 0.05),
    (5, 'I', 'SDSS z', 15.65, 0.03, 0.04),
    
    -- For Sources 6-10 (infrared data)
    (6, 'J', '2MASS J', 15.87, 0.02, 0.01),
    (6, 'H', '2MASS H', 15.45, 0.02, 0.01),
    (6, 'K', '2MASS K', 15.12, 0.01, 0.00),
    
    (7, 'J', '2MASS J', 16.23, 0.03, 0.02),
    (7, 'H', '2MASS H', 15.89, 0.02, 0.01),
    (7, 'K', '2MASS K', 15.56, 0.02, 0.01),
    
    (8, 'J', '2MASS J', 16.78, 0.03, 0.02),
    (8, 'H', '2MASS H', 16.34, 0.02, 0.01),
    (8, 'K', '2MASS K', 16.01, 0.02, 0.01),
    
    (9, 'J', '2MASS J', 17.23, 0.04, 0.02),
    (9, 'H', '2MASS H', 16.87, 0.03, 0.01),
    (9, 'K', '2MASS K', 16.45, 0.03, 0.01),
    
    (10, 'J', '2MASS J', 15.56, 0.02, 0.01),
    (10, 'H', '2MASS H', 15.12, 0.01, 0.01),
    (10, 'K', '2MASS K', 14.89, 0.01, 0.00);

-- Insert sample redshift measurements
INSERT INTO redshift_measurement (agn_id, redshift_type, z_value, z_error) VALUES
    (1, 'spectroscopic', 0.145, 0.001),
    (2, 'spectroscopic', 0.235, 0.002),
    (3, 'spectroscopic', 0.378, 0.003),
    (4, 'photometric', 0.512, 0.035),
    (5, 'spectroscopic', 0.189, 0.001),
    (6, 'spectroscopic', 0.642, 0.004),
    (7, 'spectroscopic', 0.325, 0.002),
    (8, 'photometric', 0.467, 0.042),
    (9, 'spectroscopic', 0.721, 0.005),
    (10, 'spectroscopic', 0.156, 0.001),
    (11, 'photometric', 0.389, 0.038),
    (12, 'spectroscopic', 0.567, 0.003),
    (13, 'spectroscopic', 0.298, 0.002),
    (14, 'photometric', 0.432, 0.040),
    (15, 'spectroscopic', 0.843, 0.006),
    (16, 'spectroscopic', 0.175, 0.001),
    (17, 'photometric', 0.623, 0.045),
    (18, 'spectroscopic', 0.356, 0.002),
    (19, 'spectroscopic', 0.724, 0.005),
    (20, 'photometric', 0.531, 0.044);

-- Insert sample classification data
INSERT INTO classification (agn_id, spec_class, gen_class, xray_class, best_class, image_class, sed_class) VALUES
    (1, 'BLAGN', 'Seyfert 1', 'Type 1', 'Seyfert 1', 'Point Source', 'Blue Continuum'),
    (2, 'NLAGN', 'Seyfert 2', 'Type 2', 'Seyfert 2', 'Extended', 'Red Continuum'),
    (3, 'BLAGN', 'Quasar', 'Type 1', 'Quasar', 'Point Source', 'Blue Continuum'),
    (4, NULL, 'AGN Candidate', 'Type 2', 'AGN Candidate', 'Extended', 'Red Continuum'),
    (5, 'BLAGN', 'Seyfert 1.5', 'Type 1', 'Seyfert 1.5', 'Point Source', 'Blue Continuum'),
    (6, 'BLAGN', 'Quasar', 'Type 1', 'Quasar', 'Point Source', 'Blue Continuum'),
    (7, 'NLAGN', 'Seyfert 2', 'Type 2', 'Seyfert 2', 'Extended', 'Red Continuum'),
    (8, NULL, 'AGN Candidate', 'Type 1', 'AGN Candidate', 'Point Source', 'Blue Continuum'),
    (9, 'BLAGN', 'Quasar', 'Type 1', 'Quasar', 'Point Source', 'Blue Continuum'),
    (10, 'NLAGN', 'Seyfert 2', 'Type 2', 'Seyfert 2', 'Extended', 'Red Continuum'),
    (11, NULL, 'AGN Candidate', 'Type 2', 'AGN Candidate', 'Extended', 'Red Continuum'),
    (12, 'BLAGN', 'Quasar', 'Type 1', 'Quasar', 'Point Source', 'Blue Continuum'),
    (13, 'NLAGN', 'LINER', 'Type 2', 'LINER', 'Extended', 'Red Continuum'),
    (14, NULL, 'AGN Candidate', 'Type 1', 'AGN Candidate', 'Point Source', 'Flat Continuum'),
    (15, 'BLAGN', 'Quasar', 'Type 1', 'Quasar', 'Point Source', 'Blue Continuum'),
    (16, 'NLAGN', 'Seyfert 2', 'Type 2', 'Seyfert 2', 'Extended', 'Red Continuum'),
    (17, NULL, 'AGN Candidate', 'Type 2', 'AGN Candidate', 'Extended', 'Red Continuum'),
    (18, 'BLAGN', 'Seyfert 1', 'Type 1', 'Seyfert 1', 'Point Source', 'Blue Continuum'),
    (19, 'BLAGN', 'Quasar', 'Type 1', 'Quasar', 'Point Source', 'Blue Continuum'),
    (20, 'NLAGN', 'Seyfert 2', 'Type 2', 'Seyfert 2', 'Extended', 'Red Continuum'); 