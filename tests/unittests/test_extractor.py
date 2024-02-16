from unittest.mock import MagicMock
from pydantic import BaseModel
from enum import Enum

from core.extractor import create_model, extract_columns
import pytest

# If create_model and extract_columns are defined elsewhere, ensure they're correctly imported

def test_create_model():
    """Test the create_model function."""
    column_names = ['name', 'age', 'email']
    MultiClassPrediction = create_model(column_names)
    assert issubclass(MultiClassPrediction, BaseModel), "MultiClassPrediction should be a subclass of BaseModel"
    assert 'related_columns' in MultiClassPrediction.__annotations__, "'related_columns' should be in MultiClassPrediction annotations"
    assert issubclass(MultiClassPrediction.__annotations__['related_columns'].__args__[0], Enum), "'related_columns' should be an Enum"

def test_extract_columns():
    """Test the extract_columns function with a mocked OpenAI client."""
    # Create a mock for the OpenAI client
    mock_client = MagicMock()
    mock_response_json = '{"related_columns":["Images","Images 3","Images 4","Images 5"]}'
    # Assuming model_dump_json is a method that needs to be mocked
    mock_client.chat.completions.create.return_value.model_dump_json.return_value = mock_response_json

    requirement = "All products should have four image columns"
    column_names = ['Images', 'Images 3', 'Images 4', 'Images 5']
    MultiClassPrediction = create_model(column_names)
    class_model = MultiClassPrediction

    # Call extract_columns with the mocked client
    result = extract_columns(requirement, mock_client, class_model)

    # Verify the expected methods on the mock_client were called
    mock_client.chat.completions.create.assert_called_once()

    # Verify the result
    expected_result = eval(mock_response_json)  # Using eval to convert the JSON string to a Python dict
    assert result == expected_result, "The result from extract_columns does not match the expected result"

