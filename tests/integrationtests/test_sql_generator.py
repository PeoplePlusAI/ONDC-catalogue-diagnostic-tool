import unittest
from openai import OpenAI
from core.generate_sql import generate_sql_queries
from utils.instructor_utils import patch_client
from dotenv import load_dotenv
import os

load_dotenv(
    "ops/.env"
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class TestColumnExtractorIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Initialize the OpenAI client with your API key and other configurations
        cls.client = patch_client(
            OpenAI(api_key=OPENAI_API_KEY)
        )

    def test_extract_columns_integration(self):
        """Integration test for the extract_columns function with the actual OpenAI API."""
        # Define a realistic requirement
        requirement = "All products should have four image columns"
        
        # Define column names that could be relevant to the requirement
        column_names = ['Images 1', 'Images 2', 'Images 3', 'Images 4']
        
        actual_result = {'queries': ["SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'products' AND COLUMN_NAME IN ('Images 1', 'Images 2', 'Images 3', 'Images 4');",
  'SELECT row_number() over (order by (select null)) as row_num, * FROM products WHERE `Images 1` IS NULL OR `Images 2` IS NULL OR `Images 3` IS NULL OR `Images 4` IS NULL;']}
        
        # Perform the actual API call
        result = generate_sql_queries(requirement, column_names, self.client)
        print(result)
        
        # Verify the response structure and content
        # Note: The exact content of the response may vary, so we check for the presence of expected keys or structure
        self.assertEqual(result['queries'][0].lower(), actual_result['queries'][0].lower())
        #self.assertEqual(result['queries'][1].lower(), actual_result['queries'][1].lower())

        
if __name__ == '__main__':
    unittest.main()
