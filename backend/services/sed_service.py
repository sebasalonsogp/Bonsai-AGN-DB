from typing import Optional, Tuple
import os
import uuid
from datetime import datetime
from pathlib import Path

from core.exceptions import AGNDBException
from core.logging_config import logger

class SEDService:
    """Service for handling Spectral Energy Distribution (SED) processing."""
    
    def __init__(self, sed_output_dir: str = "seds"):
        """Initialize SED service with output directory."""
        logger.info(f"Initializing SED service with output directory: {sed_output_dir}")
        self.sed_output_dir = Path(os.path.abspath(sed_output_dir))
        logger.info(f"Absolute path of output directory: {self.sed_output_dir.absolute()}")
        self.sed_output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Directory exists: {self.sed_output_dir.exists()}")
        
    async def process_sed(self, raw_data: str) -> Tuple[str, str]:
        """
        Process SED data and generate visualization.
        
        Args:
            raw_data: Space-separated wavelength,flux pairs
            
        Returns:
            Tuple of (sed_name, file_path) where:
            - sed_name: Unique identifier for the SED
            - file_path: Path to the generated SED image
            
        Raises:
            AGNDBException: If processing fails
        """
        try:
            # Generate unique SED name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_id = str(uuid.uuid4())[:8]
            sed_name = f"sed_{timestamp}_{unique_id}"
            logger.info(f"Generated SED name: {sed_name}")
            
            # Create temporary data file
            data_file = self.sed_output_dir / f"{sed_name}.txt"
            logger.info(f"Creating temporary data file at: {data_file}")
            logger.info(f"Data file absolute path: {data_file.absolute()}")
            with open(data_file, "w") as f:
                f.write(raw_data)
            logger.info(f"Data written to file: {data_file.exists()}")
            
            # Process SED data
            output_file = self.sed_output_dir / f"{sed_name}.png"
            logger.info(f"Starting SED processing for file: {data_file}")
            logger.info(f"Output will be written to: {output_file}")
            
            # Import here to avoid circular imports
            from sed_processing import process_sed_data
            
            success = process_sed_data(str(data_file), str(output_file))
            logger.info(f"SED processing completed with success: {success}")
            if not success:
                raise AGNDBException("Failed to process SED data")
            
            # Clean up temporary data file
            data_file.unlink()
            logger.info(f"Temporary data file cleaned up: {not data_file.exists()}")
            
            return sed_name, str(output_file)
            
        except Exception as e:
            logger.error(f"Error processing SED: {str(e)}")
            logger.error(f"Error occurred with data file: {data_file}")
            logger.error(f"Error occurred with output directory: {self.sed_output_dir}")
            raise AGNDBException(f"Failed to process SED: {str(e)}")
    
    async def get_sed_file(self, sed_name: str) -> Optional[Path]:
        """
        Get the path to a generated SED file.
        
        Args:
            sed_name: Name of the SED
            
        Returns:
            Path to the SED file if it exists, None otherwise
        """
        logger.info(f"Getting SED file for name: {sed_name}")
        file_path = self.sed_output_dir / f"{sed_name}.png"
        logger.info(f"Constructed file path: {file_path}")
        logger.info(f"Absolute file path: {file_path.absolute()}")
        logger.info(f"Parent directory exists: {file_path.parent.exists()}")
        logger.info(f"Parent directory contents: {list(file_path.parent.glob('*'))}")
        logger.info(f"File exists: {file_path.exists()}")
        if file_path.exists():
            logger.info(f"File size: {file_path.stat().st_size} bytes")
            logger.info(f"File permissions: {oct(file_path.stat().st_mode)}")
        return file_path if file_path.exists() else None 