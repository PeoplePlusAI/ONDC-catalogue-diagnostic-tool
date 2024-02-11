import unittest
from unittest.mock import MagicMock
from pydantic import BaseModel
from enum import Enum

from core.extractor import create_model, extract_columns

class TestColumnExtractorFunctions(unittest.TestCase):

    def test_create_model(self):
        """Test the create_model function."""
        column_names = ['name', 'age', 'email']
        MultiClassPrediction = create_model(column_names)
        self.assertTrue(issubclass(MultiClassPrediction, BaseModel))
        self.assertTrue('related_columns' in MultiClassPrediction.__annotations__)
        self.assertTrue(issubclass(MultiClassPrediction.__annotations__['related_columns'].__args__[0], Enum))

    def test_extract_columns(self):
        """Test the extract_columns function with a mocked OpenAI client."""
        # Create a mock for the OpenAI client
        mock_client = MagicMock()
        mock_response_json = '{"related_columns":["Images","Images 3","Images 4","Images 5"]}'
        # Assuming model_dump_json is a method that needs to be mocked
        mock_client.chat.completions.create.return_value.model_dump_json.return_value = mock_response_json

        # Define the requirement and model
        requirement = "All products should have four image columns"
        column_names = ['Images', 'Images 3', 'Images 4', 'Images 5']
        MultiClassPrediction = create_model(column_names)
        class_model = MultiClassPrediction

        # Call extract_columns with the mocked client
        result = extract_columns(requirement, mock_client, class_model)

        # Verify the expected methods on the mock_client were called
        mock_client.chat.completions.create.assert_called_once()
        # Since we are directly mocking the client passed as a parameter, no need to patch

        # Verify the result
        expected_result = eval(mock_response_json)  # Using eval to convert the JSON string to a Python dict
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
