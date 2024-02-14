import unittest
from openai import OpenAI
from core.extractor import create_model, extract_columns
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

    def test_extract_columns_integration_1(self):
        """Integration test for the extract_columns function with the actual OpenAI API."""
        # Define a realistic requirement
        requirement = "All products should have four image columns"
        
        # Define column names that could be relevant to the requirement
        column_names = ['Images', 'Images 3', 'Images 4', 'Images 5', 'product_id', 'product_name', 'product_description', 'other_details']
        
        # Create the model class dynamically
        MultiClassPrediction = create_model(column_names)
        
        # Perform the actual API call
        result = extract_columns(requirement, self.client, MultiClassPrediction)
        
        # Verify the response structure and content
        # Note: The exact content of the response may vary, so we check for the presence of expected keys or structure
        self.assertEqual(result['related_columns'], ['Images', 'Images 3', 'Images 4', 'Images 5'])


    def test_extract_columns_integration_2(self):
        """Integration test for the extract_columns function with the actual OpenAI API."""
        
        requirement = "All products should have short description and long description"

        # Define column names that could be relevant to the requirement
        column_names = ['Images', 'Images 3', 'Images 4', 'Images 5', 'product_id', 'product_name', 'product_description', 'other_details']
        
        # Create the model class dynamically
        MultiClassPrediction = create_model(column_names)

        result = extract_columns(requirement, self.client, MultiClassPrediction)

        self.assertEqual(result['related_columns'], ['product_description', 'other_details'])

    def test_extract_columns_integration_3(self):
        """Integration test for the extract_columns function with the actual OpenAI API."""
        
        requirement = "All products should have a product_id, product_name, product_description, and other_details"

        # Define column names that could be relevant to the requirement
        column_names = ['Images', 'Images 3', 'Images 4', 'Images 5', 'product_id', 'product_name', 'product_description', 'other_details']
        
        # Create the model class dynamically
        MultiClassPrediction = create_model(column_names)

        result = extract_columns(requirement, self.client, MultiClassPrediction)

        self.assertEqual(result['related_columns'], ["product_id", "product_name", "product_description", "other_details"])

    def test_extract_columns_integration_4(self):
        """Integration test for the extract_columns function with the actual OpenAI API."""
        
        requirement = "product name should have name, pack size and brand name"

        # Define column names that could be relevant to the requirement
        column_names = ['Images', 'Images 3', 'Images 4', 'Images 5', 'product_id', 'product_name', 'product_description', 'other_details']
        
        # Create the model class dynamically
        MultiClassPrediction = create_model(column_names)

        result = extract_columns(requirement, self.client, MultiClassPrediction)
        print(result)

        self.assertEqual(result['related_columns'], ["product_name"])

if __name__ == '__main__':
    unittest.main()
