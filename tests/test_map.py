"""
Unit tests for map.py
"""
import sys
import os
# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import Mock, patch, MagicMock
from pydantic import ValidationError

from map import geocode_address, GeocodeInput, GeocodeOutput


def test_geocode_input_validation():
    """Test GeocodeInput validation with valid data"""
    # Valid input
    valid_input = GeocodeInput(address="Tehran, Iran")
    assert valid_input.address == "Tehran, Iran"
    
    # Invalid input - missing required field
    with pytest.raises(ValidationError):
        GeocodeInput()


def test_geocode_address_successful_response():
    """Test geocode_address with a successful API response"""
    test_input = GeocodeInput(address="Tehran, Iran")
    
    mock_response = Mock()
    mock_response.json.return_value = {
        "location": {
            "y": 35.6892,
            "x": 51.3890
        }
    }
    mock_response.raise_for_status.return_value = None  # No exception
    
    with patch.dict(os.environ, {"NESHAN_API_KEY": "test_key"}), \
         patch('map.requests.get') as mock_get:
        mock_get.return_value = mock_response
        
        result = geocode_address(test_input)
        
        # Verify the result is a GeocodeOutput with the correct URL
        assert isinstance(result, GeocodeOutput)
        # The actual coordinate precision might differ, so check that the URL contains the expected elements
        assert "https://www.google.com/maps/search/?api=1&query=" in result.url
        assert "35.6892" in result.url
        assert "51.389" in result.url  # The actual response might have less precision
        
        # Verify the request was called with correct parameters
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert "https://api.neshan.org/v6/geocoding" in args[0]
        assert kwargs["params"]["address"] == "Tehran, Iran"
        assert kwargs["headers"]["Api-Key"] == "test_key"


def test_geocode_address_api_error():
    """Test geocode_address handles API errors gracefully"""
    test_input = GeocodeInput(address="Invalid Address")
    
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = Exception("API Error")
    
    with patch.dict(os.environ, {"NESHAN_API_KEY": "test_key"}), \
         patch('map.requests.get') as mock_get:
        mock_get.return_value = mock_response
        
        with pytest.raises(Exception):
            geocode_address(test_input)


def test_geocode_address_empty_response():
    """Test geocode_address when API returns empty response"""
    test_input = GeocodeInput(address="Nowhere")
    
    mock_response = Mock()
    mock_response.json.return_value = {}  # Empty response
    mock_response.raise_for_status.return_value = None
    
    with patch.dict(os.environ, {"NESHAN_API_KEY": "test_key"}), \
         patch('map.requests.get') as mock_get:
        mock_get.return_value = mock_response
        
        result = geocode_address(test_input)
        
        # Should return "Not found" for empty response
        assert isinstance(result, GeocodeOutput)
        assert result.url == "Not found"


def test_geocode_address_missing_location_data():
    """Test geocode_address when API returns response without location data"""
    test_input = GeocodeInput(address="Somewhere")
    
    mock_response = Mock()
    mock_response.json.return_value = {"other_field": "value"}  # No location field
    mock_response.raise_for_status.return_value = None
    
    with patch.dict(os.environ, {"NESHAN_API_KEY": "test_key"}), \
         patch('map.requests.get') as mock_get:
        mock_get.return_value = mock_response
        
        with pytest.raises(KeyError):
            geocode_address(test_input)


def test_geocode_address_missing_neshan_api_key():
    """Test geocode_address when NESHAN_API_KEY is not set"""
    test_input = GeocodeInput(address="Tehran, Iran")
    
    # Mock the response
    mock_response = Mock()
    mock_response.json.return_value = {
        "location": {
            "y": 35.6892,
            "x": 51.3890
        }
    }
    mock_response.raise_for_status.return_value = None
    
    # Temporarily remove NESHAN_API_KEY from environment
    original_key = os.environ.pop("NESHAN_API_KEY", None)
    
    try:
        with patch('map.requests.get') as mock_get:
            mock_get.return_value = mock_response
            
            # Since we're patching requests, this will still succeed but with None as Api-Key
            result = geocode_address(test_input)
            
            # Verify the request was called with the correct headers (Api-Key should be None)
            mock_get.assert_called_once()
            _, kwargs = mock_get.call_args
            assert kwargs["headers"]["Api-Key"] is None
    finally:
        # Restore the original key if it existed
        if original_key:
            os.environ["NESHAN_API_KEY"] = original_key