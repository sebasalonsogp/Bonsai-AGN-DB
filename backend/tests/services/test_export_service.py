import pytest
import csv
import io
import xml.etree.ElementTree as ET
from services.export_service import ExportService

# Sample test data
sample_data = [
    {
        "agn_id": "AGN001",
        "ra": 14.5,
        "declination": -23.2,
        "band_label": "g",
        "mag_value": 19.3
    },
    {
        "agn_id": "AGN002",
        "ra": 15.7,
        "declination": -22.1,
        "band_label": "r",
        "mag_value": 18.7
    }
]


@pytest.mark.asyncio
async def test_export_to_csv():
    """Test exporting data to CSV format."""
    # Export with default options
    csv_content = await ExportService.export_to_csv(sample_data)
    
    # Parse CSV
    reader = csv.reader(io.StringIO(csv_content))
    rows = list(reader)
    
    # Check that metadata is included (first 5 rows)
    assert rows[0][0].startswith("# AGN-DB Export")
    assert rows[1][0].startswith("# Generated:")
    assert rows[2][0].startswith("# Fields:")
    assert rows[3][0].startswith("# Total records:")
    
    # Check header row and content rows
    header_row = rows[5]  # After metadata
    assert set(header_row) == {"agn_id", "ra", "declination", "band_label", "mag_value"}
    
    # Check data rows
    data_rows = rows[6:]
    assert len(data_rows) == 2
    
    # Test without metadata
    csv_content_no_meta = await ExportService.export_to_csv(sample_data, include_metadata=False)
    reader = csv.reader(io.StringIO(csv_content_no_meta))
    rows = list(reader)
    
    # First row should be header
    assert rows[0] == header_row
    
    # Test with selected fields
    selected_fields = ["agn_id", "ra", "declination"]
    csv_content_selected = await ExportService.export_to_csv(sample_data, selected_fields=selected_fields)
    reader = csv.reader(io.StringIO(csv_content_selected))
    rows = list(reader)
    
    # Check that only selected fields are included in header
    header_row = rows[5]  # After metadata
    assert set(header_row) == set(selected_fields)


@pytest.mark.asyncio
async def test_export_to_votable():
    """Test exporting data to VOTable format."""
    # Export with default options
    votable_content = await ExportService.export_to_votable(sample_data)
    
    # Parse VOTable
    root = ET.fromstring(votable_content)
    
    # Check namespace
    assert root.tag.endswith('VOTABLE')
    assert 'version' in root.attrib
    
    # Check RESOURCE element
    resource = root.find('.//{*}RESOURCE')
    assert resource is not None
    assert resource.attrib.get('name') == 'AGN-DB Export'
    
    # Check TABLE element
    table = resource.find('.//{*}TABLE')
    assert table is not None
    
    # Check FIELD elements
    fields = table.findall('.//{*}FIELD')
    assert len(fields) == 5  # Number of unique fields in sample data
    field_names = [field.attrib.get('name') for field in fields]
    assert set(field_names) == {"agn_id", "ra", "declination", "band_label", "mag_value"}
    
    # Check DATA/TABLEDATA
    tabledata = table.find('.//{*}TABLEDATA')
    assert tabledata is not None
    
    # Check rows
    rows = tabledata.findall('.//{*}TR')
    assert len(rows) == 2  # Number of data rows
    
    # Test with selected fields
    selected_fields = ["agn_id", "ra"]
    votable_content_selected = await ExportService.export_to_votable(sample_data, selected_fields=selected_fields)
    
    # Parse VOTable
    root = ET.fromstring(votable_content_selected)
    
    # Check FIELD elements
    table = root.find('.//{*}TABLE')
    fields = table.findall('.//{*}FIELD')
    assert len(fields) == 2  # Number of selected fields
    field_names = [field.attrib.get('name') for field in fields]
    assert set(field_names) == set(selected_fields)


@pytest.mark.asyncio
async def test_infer_votable_datatype():
    """Test datatype inference for VOTable fields."""
    # Test integer datatype
    int_data = [{"field1": 1}, {"field1": 2}]
    assert ExportService._infer_votable_datatype(int_data, "field1") == "int"
    
    # Test double datatype
    double_data = [{"field1": 1.5}, {"field1": 2.7}]
    assert ExportService._infer_votable_datatype(double_data, "field1") == "double"
    
    # Test string datatype
    string_data = [{"field1": "value1"}, {"field1": "value2"}]
    assert ExportService._infer_votable_datatype(string_data, "field1") == "char"
    
    # Test mixed datatype (should default to char)
    mixed_data = [{"field1": 1}, {"field1": "value"}]
    assert ExportService._infer_votable_datatype(mixed_data, "field1") == "char"
    
    # Test empty data
    empty_data = [{"field2": 1}]
    assert ExportService._infer_votable_datatype(empty_data, "field1") == "char" 