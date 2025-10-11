# Tests for Tourism Chatbot

This directory contains unit tests for the tourism chatbot application.

## Test Structure

- `test_main.py` - Tests for the main application logic
- `test_map.py` - Tests for the geocoding functionality
- `test_docx2md.py` - Tests for DOCX to Markdown conversion utilities
- `test_text_processing.py` - Tests for text processing utilities
- `test_input_adapter.py` - Tests for the input adapter
- `conftest.py` - Pytest configuration and fixtures

## Running Tests

### Prerequisites

Make sure you have the testing dependencies installed:

```bash
pip install pytest
```

### Running All Tests

To run all tests in the suite:

```bash
pytest
```

### Running Tests with Verbose Output

To see more detailed output:

```bash
pytest -v
```

### Running Specific Test Files

To run tests for a specific module:

```bash
pytest tests/test_main.py
pytest tests/test_map.py
pytest tests/test_docx2md.py
pytest tests/test_text_processing.py
pytest tests/test_input_adapter.py
```

### Running Tests with Coverage

To run tests and generate coverage report:

```bash
pip install pytest-cov
pytest --cov=.
```

## Test Coverage

The test suite currently includes:

- **main.py**: Basic import tests (with skip for missing dependencies)
- **map.py**: Comprehensive tests for geocoding functionality including:
  - Input validation
  - Successful API response handling
  - Error handling (API errors, empty responses)
  - Missing data handling
  - Environment variable handling
- **utils/docx2md.py**: Tests for document conversion utilities including:
  - HTML conversion from DOCX
  - Markdown conversion from DOCX
  - Exception handling
  - File output functionality
  - Verbose mode
- **utils/input_adapter.py**: Tests for input loading including:
  - Raw text loading
  - File extension support
  - Error handling for unsupported formats
  - Input validation
- **utils/text_processing.py**: Tests for text processing including:
  - Persian text cleaning
  - Heading detection
  - Header addition
  - Text chunking
  - Metadata attachment

## Test Configuration

The `conftest.py` file contains shared fixtures and configuration:
- Environment variables are automatically set for testing
- Common test fixtures are available for mocking components
- Default test settings are configured

## Adding New Tests

When adding new functionality to the application, please add corresponding tests in this directory following the naming convention `test_*.py`. Use the existing test files as examples for properly structured unit tests with appropriate mocking and assertions.