import pytest
from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch, MagicMock, AsyncMock

client = TestClient(app)


@pytest.fixture
def mock_repo_and_service():
    """Mock repository and export service for integration testing."""
    with patch("api.v1.queries.search.search_repo") as mock_repo:
        with patch("api.v1.queries.search.export_service") as mock_service:
            # Setup mock data
            mock_data = [
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
            # Use AsyncMock for async methods
            mock_repo.execute_query = AsyncMock(return_value=(mock_data, 2))
            
            # Setup mock export services with AsyncMock
            mock_service.export_to_csv = AsyncMock(return_value="agn_id,ra,declination\nAGN001,14.5,-23.2\nAGN002,15.7,-22.1")
            mock_service.export_to_votable = AsyncMock(return_value="<VOTABLE>...</VOTABLE>")
            
            yield mock_repo, mock_service


def test_export_to_csv_integration(mock_repo_and_service):
    """Test the complete export to CSV pipeline."""
    mock_repo, mock_service = mock_repo_and_service
    
    # Prepare test data
    query = {"combinator": "and", "rules": []}
    export_options = {
        "format": "csv",
        "selected_fields": ["agn_id", "ra", "declination"],
        "include_metadata": True
    }
    
    # Send request to the export endpoint
    response = client.post(
        "/api/v1/search/export",
        json={
            "query": query,
            "export_options": export_options
        }
    )
    
    # Check response
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/csv"  # Now should match exactly
    assert response.headers["Content-Disposition"] == "attachment; filename=agn_db_export.csv"
    
    # Verify mock calls
    mock_repo.execute_query.assert_called_once()
    mock_service.export_to_csv.assert_called_once_with(
        mock_repo.execute_query.return_value[0],
        selected_fields=export_options["selected_fields"],
        include_metadata=export_options["include_metadata"]
    )


def test_export_to_votable_integration(mock_repo_and_service):
    """Test the complete export to VOTable pipeline."""
    mock_repo, mock_service = mock_repo_and_service
    
    # Prepare test data
    query = {"combinator": "and", "rules": []}
    export_options = {
        "format": "votable",
        "selected_fields": ["agn_id", "ra", "declination"],
        "include_metadata": True
    }
    
    # Send request to the export endpoint
    response = client.post(
        "/api/v1/search/export",
        json={
            "query": query,
            "export_options": export_options
        }
    )
    
    # Check response
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/xml"  # Now should match exactly
    assert response.headers["Content-Disposition"] == "attachment; filename=agn_db_export.xml"
    
    # Verify mock calls
    mock_repo.execute_query.assert_called_once()
    mock_service.export_to_votable.assert_called_once_with(
        mock_repo.execute_query.return_value[0],
        selected_fields=export_options["selected_fields"],
        include_metadata=export_options["include_metadata"]
    )


def test_get_available_fields_integration(mock_repo_and_service):
    """Test the get available fields endpoint."""
    mock_repo, _ = mock_repo_and_service
    
    # Send request to the available fields endpoint
    response = client.get("/api/v1/search/available-fields")
    
    # Check response
    assert response.status_code == 200
    assert "categories" in response.json()
    assert "all_fields" in response.json()
    
    # Verify mock calls
    mock_repo.execute_query.assert_called_once()


def test_export_with_invalid_format_integration(mock_repo_and_service):
    """Test export with invalid format."""
    # Prepare test data with invalid format
    query = {"combinator": "and", "rules": []}
    export_options = {
        "format": "invalid_format",
        "selected_fields": ["agn_id", "ra", "declination"],
        "include_metadata": True
    }
    
    # Send request to the export endpoint
    response = client.post(
        "/api/v1/search/export",
        json={
            "query": query,
            "export_options": export_options
        }
    )
    
    # Check response - FastAPI returns 422 Unprocessable Entity for schema validation failures
    assert response.status_code == 422
    
    # Verify validation error details based on the actual response structure
    response_json = response.json()
    assert response_json["detail"] == "Validation error"
    assert response_json["status_code"] == 422
    assert any("format" in str(error["loc"]) for error in response_json["errors"]) 