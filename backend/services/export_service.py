import csv
import io
from typing import Any, Dict, List, Optional, Set
from loguru import logger
import xml.etree.ElementTree as ET
from datetime import datetime


class ExportService:
    """Service for exporting data to various formats (CSV, VOTable)."""
    
    @staticmethod
    async def export_to_csv(
        data: List[Dict[str, Any]],
        selected_fields: Optional[List[str]] = None,
        include_metadata: bool = True
    ) -> str:
        """
        Export data to CSV format.
        
        Args:
            data: List of dictionaries containing the data to export
            selected_fields: Optional list of fields to include in the export
            include_metadata: Whether to include metadata headers
            
        Returns:
            CSV content as a string
        """
        if not data:
            return ""
            
        # Determine fields to export
        all_fields = set()
        for item in data:
            all_fields.update(item.keys())
            
        # Use selected fields if provided, otherwise use all fields
        fields_to_export = selected_fields if selected_fields else sorted(list(all_fields))
        
        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Add metadata if requested
        if include_metadata:
            writer.writerow(["# AGN-DB Export"])
            writer.writerow([f"# Generated: {datetime.utcnow().isoformat()}"])
            writer.writerow([f"# Fields: {', '.join(fields_to_export)}"])
            writer.writerow([f"# Total records: {len(data)}"])
            writer.writerow(["# "])
        
        # Write header row
        writer.writerow(fields_to_export)
        
        # Write data rows
        for item in data:
            row = [item.get(field, "") for field in fields_to_export]
            writer.writerow(row)
            
        return output.getvalue()
    
    @staticmethod
    async def export_to_votable(
        data: List[Dict[str, Any]],
        selected_fields: Optional[List[str]] = None,
        include_metadata: bool = True
    ) -> str:
        """
        Export data to VOTable XML format.
        
        VOTable is an XML format defined for astronomical data interchange.
        See: https://www.ivoa.net/documents/VOTable/
        
        Args:
            data: List of dictionaries containing the data to export
            selected_fields: Optional list of fields to include in the export
            include_metadata: Whether to include metadata information
            
        Returns:
            VOTable content as a string
        """
        if not data:
            return ""
            
        # Determine fields to export
        all_fields = set()
        for item in data:
            all_fields.update(item.keys())
            
        # Use selected fields if provided, otherwise use all fields
        fields_to_export = selected_fields if selected_fields else sorted(list(all_fields))
        
        # Infer data types for each field
        field_types = {}
        for field in fields_to_export:
            field_types[field] = ExportService._infer_votable_datatype(data, field)
            
        # Create VOTable XML
        votable = ET.Element('VOTABLE', {
            'version': '1.4',
            'xmlns': 'http://www.ivoa.net/xml/VOTable/v1.4',
            'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
            'xsi:schemaLocation': 'http://www.ivoa.net/xml/VOTable/v1.4 http://www.ivoa.net/xml/VOTable/v1.4'
        })
        
        # Add RESOURCE element
        resource = ET.SubElement(votable, 'RESOURCE', {'name': 'AGN-DB Export'})
        
        # Add DESCRIPTION if metadata is included
        if include_metadata:
            description = ET.SubElement(resource, 'DESCRIPTION')
            description.text = f"Data exported from AGN-DB on {datetime.utcnow().isoformat()}"
            
        # Add TABLE element
        table = ET.SubElement(resource, 'TABLE', {'name': 'results'})
        
        # Add FIELD elements
        for field in fields_to_export:
            ET.SubElement(table, 'FIELD', {
                'name': field,
                'datatype': field_types[field],
                'ID': field
            })
            
        # Add DATA and TABLEDATA elements
        data_elem = ET.SubElement(table, 'DATA')
        tabledata = ET.SubElement(data_elem, 'TABLEDATA')
        
        # Add TR and TD elements for each row of data
        for item in data:
            tr = ET.SubElement(tabledata, 'TR')
            for field in fields_to_export:
                td = ET.SubElement(tr, 'TD')
                value = item.get(field, "")
                td.text = str(value) if value is not None else ""
                
        # Convert to string
        return ET.tostring(votable, encoding='unicode', method='xml')
        
    @staticmethod
    def _infer_votable_datatype(data: List[Dict[str, Any]], field: str) -> str:
        """
        Infer the VOTable datatype for a field based on its values.
        
        Args:
            data: List of dictionaries containing the data
            field: Field name to infer type for
            
        Returns:
            VOTable datatype string
        """
        # Collect non-None values
        values = [item.get(field) for item in data if field in item and item[field] is not None]
        
        if not values:
            return "char"
            
        # Check if all values are numeric
        try:
            if all(isinstance(v, (int, float)) or (isinstance(v, str) and v.replace('.', '', 1).isdigit()) for v in values):
                # Check if all values are integers
                if all(isinstance(v, int) or (isinstance(v, str) and v.isdigit()) for v in values):
                    return "int"
                return "double"
        except:
            pass
            
        # Default to character type
        return "char" 