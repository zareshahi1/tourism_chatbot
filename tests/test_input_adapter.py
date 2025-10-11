"""
Unit tests for utils/input_adapter.py
"""
import sys
import os
# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import Mock, patch, MagicMock

# Only import if available, else skip tests
try:
    from utils.input_adapter import load_input
    INPUT_ADAPTER_AVAILABLE = True
except ImportError:
    INPUT_ADAPTER_AVAILABLE = False


@pytest.mark.skipif(not INPUT_ADAPTER_AVAILABLE, reason="input_adapter module not available")
def test_load_input_with_raw_text():
    """Test load_input function with raw text provided"""
    with patch('utils.input_adapter.LOADERS') as mock_loaders:
        mock_raw_loader = Mock()
        mock_raw_loader.load.return_value = "Processed raw text"
        mock_loaders.__getitem__.return_value = mock_raw_loader
        
        result = load_input(raw_text="Original raw text")
        
        # Verify the raw loader was used correctly
        mock_raw_loader.load.assert_called_once_with(text="Original raw text")
        assert result == "Processed raw text"


@pytest.mark.skipif(not INPUT_ADAPTER_AVAILABLE, reason="input_adapter module not available")
def test_load_input_with_supported_file_extension():
    """Test load_input function with a supported file extension"""
    with patch('utils.input_adapter.LOADERS') as mock_loaders:
        mock_pdf_loader = Mock()
        mock_pdf_loader.load.return_value = "Extracted PDF content"
        mock_loaders.__getitem__.return_value = mock_pdf_loader
        mock_loaders.__contains__.return_value = True
        
        result = load_input(file_path="document.pdf")
        
        # Verify the PDF loader was used correctly
        mock_pdf_loader.load.assert_called_once_with(path="document.pdf")
        assert result == "Extracted PDF content"


@pytest.mark.skipif(not INPUT_ADAPTER_AVAILABLE, reason="input_adapter module not available")
def test_load_input_with_unsupported_file_extension():
    """Test load_input function with an unsupported file extension"""
    with patch('utils.input_adapter.LOADERS') as mock_loaders:
        mock_loaders.__contains__.return_value = False
        
        with pytest.raises(ValueError, match=r"\.xyz is not supported format"):
            load_input(file_path="document.xyz")


@pytest.mark.skipif(not INPUT_ADAPTER_AVAILABLE, reason="input_adapter module not available")
def test_load_input_with_no_input():
    """Test load_input function when neither file_path nor raw_text is provided"""
    with pytest.raises(ValueError, match=r"file path or raw text required"):
        load_input()


@pytest.mark.skipif(not INPUT_ADAPTER_AVAILABLE, reason="input_adapter module not available")
def test_load_input_with_both_inputs():
    """Test load_input function when both file_path and raw_text are provided"""
    # When both are provided, raw_text should take precedence
    with patch('utils.input_adapter.LOADERS') as mock_loaders:
        mock_raw_loader = Mock()
        mock_raw_loader.load.return_value = "Processed raw text"
        mock_loaders.__getitem__.return_value = mock_raw_loader
        
        result = load_input(file_path="document.pdf", raw_text="Raw text")
        
        # Raw text should take precedence
        mock_raw_loader.load.assert_called_once_with(text="Raw text")
        assert result == "Processed raw text"


@pytest.mark.skipif(not INPUT_ADAPTER_AVAILABLE, reason="input_adapter module not available")
def test_load_input_different_extensions():
    """Test load_input function with different supported file extensions"""
    extensions = [".docx", ".pdf", ".txt", ".md", ".html", ".htm"]
    
    for ext in extensions:
        with patch('utils.input_adapter.LOADERS') as mock_loaders:
            mock_loader = Mock()
            mock_loader.load.return_value = f"Content from {ext} file"
            mock_loaders.__getitem__.return_value = mock_loader
            mock_loaders.__contains__.return_value = True
            
            result = load_input(file_path=f"document{ext}")
            
            # Verify the appropriate loader was used
            mock_loader.load.assert_called_once_with(path=f"document{ext}")
            assert result == f"Content from {ext} file"