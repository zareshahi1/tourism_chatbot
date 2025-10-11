"""
Pytest configuration and fixtures for the test suite
"""
import os
import sys
import pytest
from unittest.mock import Mock, patch
from io import StringIO


@pytest.fixture(autouse=True)
def set_test_environment():
    """Set up test environment variables"""
    original_env = os.environ.copy()
    
    # Set minimal required environment variables for testing
    os.environ["NESHAN_API_KEY"] = "test_neshan_key"
    os.environ["OPENAI_API_KEY"] = "test_openai_key"
    os.environ["JINA_API_KEY"] = "test_jina_key"
    
    yield
    
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def mock_openai_model():
    """Mock OpenAI model for testing"""
    with patch('main.ChatOpenAI') as mock:
        instance = Mock()
        instance.bind_tools = Mock(return_value=instance)
        mock.return_value = instance
        yield instance


@pytest.fixture
def sample_text_document():
    """Sample text for testing"""
    return """This is a sample text document.
    It contains multiple lines.
    Some of these lines are paragraphs.
    Others might be lists:
    - First item
    - Second item
    Or tables:
    | Column 1 | Column 2 |
    |----------|----------|
    | Data 1   | Data 2   |"""


@pytest.fixture
def sample_docx_bytes():
    """Sample bytes for mocking DOCX files"""
    return b"fake docx content"


@pytest.fixture
def temp_test_file(tmp_path):
    """Create a temporary test file"""
    test_file = tmp_path / "test.txt"
    test_file.write_text("This is test content", encoding="utf-8")
    return str(test_file)


@pytest.fixture
def mock_langchain_messages():
    """Mock langchain message objects"""
    with patch('main.HumanMessage') as mock_human, \
         patch('main.SystemMessage') as mock_system, \
         patch('main.ToolMessage') as mock_tool:
        
        yield {
            'HumanMessage': mock_human,
            'SystemMessage': mock_system,
            'ToolMessage': mock_tool
        }