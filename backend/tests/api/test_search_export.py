import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi import HTTPException
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.queries.search import export_search_results, get_available_fields
from schemas import ExportFormat, ExportOptions


@pytest.fixture
def mock_db():
    """Mock database session."""
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def mock_search_repo():
    """Mock search repository."""
    with patch("api.v1.queries.search.search_repo") as mock:
        # Setup mock return value for execute_query
        mock.execute_query = AsyncMock(return_value=(
            [
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
            ],
            2
        ))
        yield mock


@pytest.fixture
def mock_export_service():
    """Mock export service."""
    with patch("api.v1.queries.search.export_service") as mock:
        # Setup mock return values for export methods
        mock.export_to_csv = AsyncMock(return_value="agn_id,ra,declination\nAGN001,14.5,-23.2\nAGN002,15.7,-22.1")
        mock.export_to_votable = AsyncMock(return_value="<VOTABLE>...</VOTABLE>")
        yield mock


@pytest.mark.asyncio
async def test_export_search_results_csv(mock_db, mock_search_repo, mock_export_service):
    """Test exporting search results to CSV."""
    # Test data
    query = {"combinator": "and", "rules": []}
    export_options = ExportOptions(
        format=ExportFormat.CSV,
        selected_fields=["agn_id", "ra", "declination"],
        include_metadata=True
    )
    
    # Call the endpoint function directly
    response = await export_search_results(query, export_options, mock_db)
    
    # Verify search repository was called
    mock_search_repo.execute_query.assert_called_once_with(
        mock_db, query, skip=0, limit=10000
    )
    
    # Verify export service was called with correct arguments
    mock_export_service.export_to_csv.assert_called_once_with(
        mock_search_repo.execute_query.return_value[0],
        selected_fields=export_options.selected_fields,
        include_metadata=export_options.include_metadata
    )
    
    # Check response
    assert response.status_code == 200
    assert response.headers["Content-Disposition"] == "attachment; filename=agn_db_export.csv"
    assert response.media_type == "text/csv"


@pytest.mark.asyncio
async def test_export_search_results_votable(mock_db, mock_search_repo, mock_export_service):
    """Test exporting search results to VOTable."""
    # Test data
    query = {"combinator": "and", "rules": []}
    export_options = ExportOptions(
        format=ExportFormat.VOTABLE,
        selected_fields=["agn_id", "ra", "declination"],
        include_metadata=True
    )
    
    # Call the endpoint function directly
    response = await export_search_results(query, export_options, mock_db)
    
    # Verify search repository was called
    mock_search_repo.execute_query.assert_called_once_with(
        mock_db, query, skip=0, limit=10000
    )
    
    # Verify export service was called with correct arguments
    mock_export_service.export_to_votable.assert_called_once_with(
        mock_search_repo.execute_query.return_value[0],
        selected_fields=export_options.selected_fields,
        include_metadata=export_options.include_metadata
    )
    
    # Check response
    assert response.status_code == 200
    assert response.headers["Content-Disposition"] == "attachment; filename=agn_db_export.xml"
    assert response.media_type == "application/xml"


@pytest.mark.asyncio
async def test_export_search_results_unsupported_format(mock_db, mock_search_repo):
    """
    Test exporting search results with unsupported format.
    
    Note: In unit tests we test the handler function directly which returns 400,
    but in integration tests we get 422 because FastAPI's Pydantic validation
    intercepts the request before it reaches our handler.
    """
    # Test data with invalid format
    query = {"combinator": "and", "rules": []}
    export_options = MagicMock()
    export_options.format = "unsupported_format"
    
    # Patch the export service and repository to isolate the format validation
    with patch("api.v1.queries.search.export_service"):
        # Expect exception
        with pytest.raises(HTTPException) as excinfo:
            await export_search_results(query, export_options, mock_db)
        
        # Check exception details - now properly preserving the 400 status code
        assert excinfo.value.status_code == 400
        assert "Unsupported export format" in excinfo.value.detail


@pytest.mark.asyncio
async def test_export_search_results_db_error(mock_db, mock_search_repo):
    """Test handling database errors in export endpoint."""
    # Setup error
    mock_search_repo.execute_query.side_effect = Exception("Database error")
    
    # Test data
    query = {"combinator": "and", "rules": []}
    export_options = ExportOptions(
        format=ExportFormat.CSV,
        selected_fields=["agn_id", "ra", "declination"],
        include_metadata=True
    )
    
    # Expect exception
    with pytest.raises(HTTPException) as excinfo:
        await export_search_results(query, export_options, mock_db)
    
    # Check exception details
    assert excinfo.value.status_code == 500
    assert "Export failed" in excinfo.value.detail


@pytest.mark.asyncio
async def test_get_available_fields(mock_db, mock_search_repo):
    """Test getting available fields for export."""
    # Call the endpoint function directly
    result = await get_available_fields(mock_db)
    
    # Verify search repository was called
    mock_search_repo.execute_query.assert_called_once_with(
        mock_db, {}, limit=10
    )
    
    # Check result structure
    assert "categories" in result
    assert "all_fields" in result
    assert isinstance(result["categories"], dict)
    assert isinstance(result["all_fields"], list)
    
    # Check categories
    assert "source" in result["categories"]
    assert "photometry" in result["categories"]
    assert "redshift" in result["categories"]
    assert "classification" in result["categories"]


@pytest.mark.asyncio
async def test_get_available_fields_error(mock_db, mock_search_repo):
    """Test handling errors in get available fields endpoint."""
    # Setup error
    mock_search_repo.execute_query.side_effect = Exception("Database error")
    
    # Expect exception
    with pytest.raises(HTTPException) as excinfo:
        await get_available_fields(mock_db)
    
    # Check exception details
    assert excinfo.value.status_code == 500
    assert "Failed to get available fields" in excinfo.value.detail 