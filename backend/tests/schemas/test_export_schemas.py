import pytest
from pydantic import ValidationError
from schemas import ExportFormat, ExportOptions


def test_export_format_enum():
    """Test the ExportFormat enum values."""
    assert ExportFormat.CSV == "csv"
    assert ExportFormat.VOTABLE == "votable"
    
    # Test validation with valid values
    assert ExportFormat("csv") == ExportFormat.CSV
    assert ExportFormat("votable") == ExportFormat.VOTABLE
    
    # Test validation with invalid value
    with pytest.raises(ValueError):
        ExportFormat("invalid_format")


def test_export_options_defaults():
    """Test ExportOptions with default values."""
    options = ExportOptions()
    
    assert options.format == ExportFormat.CSV
    assert options.selected_fields is None
    assert options.include_metadata is True


def test_export_options_custom_values():
    """Test ExportOptions with custom values."""
    options = ExportOptions(
        format=ExportFormat.VOTABLE,
        selected_fields=["agn_id", "ra", "declination"],
        include_metadata=False
    )
    
    assert options.format == ExportFormat.VOTABLE
    assert options.selected_fields == ["agn_id", "ra", "declination"]
    assert options.include_metadata is False


def test_export_options_validation():
    """Test ExportOptions validation."""
    # Test with invalid format
    with pytest.raises(ValidationError):
        ExportOptions(format="invalid_format")
    
    # Test with invalid selected_fields type
    with pytest.raises(ValidationError):
        ExportOptions(selected_fields="not_a_list")
    
    # Test with invalid include_metadata type
    with pytest.raises(ValidationError):
        ExportOptions(include_metadata="not_a_boolean")


def test_export_options_from_dict():
    """Test creating ExportOptions from dict."""
    data = {
        "format": "votable",
        "selected_fields": ["agn_id", "ra"],
        "include_metadata": False
    }
    
    options = ExportOptions.parse_obj(data)
    
    assert options.format == ExportFormat.VOTABLE
    assert options.selected_fields == ["agn_id", "ra"]
    assert options.include_metadata is False 