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
        self.sed_output_dir = Path(sed_output_dir)
        self.sed_output_dir.mkdir(parents=True, exist_ok=True)
        
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
            
            # Create temporary data file
            data_file = self.sed_output_dir / f"{sed_name}.txt"
            with open(data_file, "w") as f:
                f.write(raw_data)
            
            # Process SED data
            output_file = self.sed_output_dir / f"{sed_name}.png"
            
            # Import here to avoid circular imports
            from sed_processing import process_sed_data
            
            success = process_sed_data(str(data_file), str(output_file))
            if not success:
                raise AGNDBException("Failed to process SED data")
            
            # Clean up temporary data file
            data_file.unlink()
            
            return sed_name, str(output_file)
            
        except Exception as e:
            logger.error(f"Error processing SED: {str(e)}")
            raise AGNDBException(f"Failed to process SED: {str(e)}")
    
    async def get_sed_file(self, sed_name: str) -> Optional[Path]:
        """
        Get the path to a generated SED file.
        
        Args:
            sed_name: Name of the SED
            
        Returns:
            Path to the SED file if it exists, None otherwise
        """
        file_path = self.sed_output_dir / f"{sed_name}.png"
        return file_path if file_path.exists() else None 