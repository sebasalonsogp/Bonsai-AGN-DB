from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, quoted_name
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class SourceAGN(Base):
    """
    Primary model representing an Active Galactic Nucleus (AGN) source.
    
    This is the central entity in the database that other measurements
    and classifications reference. Each source represents a distinct
    astronomical object with its sky coordinates.
    """
    
    __tablename__ = "source_agn"
    
    # Primary key
    agn_id = Column(Integer, primary_key=True, index=True)
    
    # Coordinates
    ra = Column(Float, nullable=False, index=True)  # Right Ascension in degrees (0-360)
    declination = Column(Float, nullable=False, index=True)  # Declination in degrees (-90 to +90)
    
    # Relationships - each source can have multiple related records in other tables
    photometry = relationship("Photometry", back_populates="source", cascade="all, delete-orphan")
    redshift_measurements = relationship("RedshiftMeasurement", back_populates="source", cascade="all, delete-orphan")
    classifications = relationship("Classification", back_populates="source", cascade="all, delete-orphan")
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Photometry(Base):
    """
    Model representing photometric measurements of an AGN source.
    
    Photometry records store brightness measurements in various
    wavelength bands and filters. Each source may have multiple
    photometric measurements across different bands.
    """
    
    __tablename__ = "photometry"
    
    # Primary key
    phot_id = Column(Integer, primary_key=True, index=True)
    
    # Foreign key to SourceAGN - cascading delete ensures orphaned records are removed
    agn_id = Column(Integer, ForeignKey("source_agn.agn_id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Photometric data
    band_label = Column(String(50), nullable=False)  # Observational band (e.g., 'optical', 'radio', 'X-ray')
    filter_name = Column(String(100), nullable=False)  # Specific filter used (e.g., 'SDSS-g', 'Johnson-V')
    mag_value = Column(Float)  # Magnitude value (brightness measurement)
    mag_error = Column(Float)  # Error/uncertainty in the magnitude measurement
    extinction = Column(Float)  # Extinction correction value
    
    # Relationship back to source
    source = relationship("SourceAGN", back_populates="photometry")
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class RedshiftMeasurement(Base):
    """
    Model representing redshift measurements of an AGN source.
    
    Redshift is a critical measurement in astronomy that indicates
    the object's distance and recessional velocity. Each source
    may have multiple redshift measurements from different methods.
    """
    
    __tablename__ = "redshift_measurement"
    
    # Primary key
    redshift_id = Column(Integer, primary_key=True, index=True)
    
    # Foreign key to SourceAGN
    agn_id = Column(Integer, ForeignKey("source_agn.agn_id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Redshift data
    redshift_type = Column(String(50), nullable=False)  # Measurement method (e.g., 'spectroscopic', 'photometric')
    z_value = Column(Float, nullable=False)  # Redshift value
    z_error = Column(Float)  # Error/uncertainty in the redshift measurement
    
    # Relationship back to source
    source = relationship("SourceAGN", back_populates="redshift_measurements")
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Classification(Base):
    """
    Model representing various classifications of an AGN source.
    
    Classifications categorize AGNs based on different observational
    and physical characteristics. Multiple classification schemes
    can be applied to a single source (spectroscopic, morphological, etc.).
    """
    
    __tablename__ = "classification"
    
    # Primary key
    class_id = Column(Integer, primary_key=True, index=True)
    
    # Foreign key to SourceAGN
    agn_id = Column(Integer, ForeignKey("source_agn.agn_id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Classification data - each representing a different classification scheme
    spec_class = Column(String(50))  # Spectroscopic classification (e.g., 'Seyfert 1', 'Quasar')
    gen_class = Column(String(50))  # General AGN type classification
    xray_class = Column(String(50))  # X-ray based classification
    best_class = Column(String(50))  # Best/consensus classification from multiple methods
    image_class = Column(String(50))  # Morphological/image-based classification
    sed_class = Column(String(50))  # Spectral Energy Distribution based classification
    
    # Relationship back to source
    source = relationship("SourceAGN", back_populates="classifications")
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 