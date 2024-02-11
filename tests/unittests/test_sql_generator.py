import json
import unittest
from unittest.mock import MagicMock



from core.generate_sql import generate_sql_queries

class TestColumnExtractorFunctions(unittest.TestCase):
    def test_generate_sql(self):
        """Test the extract_columns function with a mocked OpenAI client."""
        # Create a mock for the OpenAI client
        mock_client = MagicMock()
        mock_response = {'queries': ["SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'products' AND COLUMN_NAME IN ('Images 1', 'Images 2', 'Images 3', 'Images 4');",
  'SELECT row_number() over (order by (select null)) as row_num, * FROM products WHERE `Images 1` IS NULL OR `Images 2` IS NULL OR `Images 3` IS NULL OR `Images 4` IS NULL;']} 
        mock_response_json = json.dumps(mock_response)
        # Assuming model_dump_json is a method that needs to be mocked
        mock_client.chat.completions.create.return_value.model_dump_json.return_value = mock_response_json

        # Define the requirement and model
        requirement = "All products should have four image columns"
        column_names = ['Images 1', 'Images 2', 'Images 3', 'Images 4']

        # Call extract_columns with the mocked client
        result = generate_sql_queries(requirement, column_names, mock_client)

        # Verify the expected methods on the mock_client were called
        mock_client.chat.completions.create.assert_called_once()
        # Since we are directly mocking the client passed as a parameter, no need to patch

        # Verify the result
        expected_result = eval(mock_response_json)  # Using eval to convert the JSON string to a Python dict
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
