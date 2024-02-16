import pytest
from openai import OpenAI
from core.generate_sql import generate_sql_queries
from utils.instructor_utils import patch_client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv("ops/.env")

@pytest.fixture(scope="module")
def openai_client():
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    # Initialize and return the patched OpenAI client
    return patch_client(OpenAI(api_key=OPENAI_API_KEY))

def test_extract_columns_integration(openai_client):
    """Integration test for the extract_columns function with the actual OpenAI API."""
    # Define a realistic requirement
    requirement = "All products should have four image columns"
    
    # Define column names that could be relevant to the requirement
    column_names = ['Images 1', 'Images 2', 'Images 3', 'Images 4']
    
    # Expected result for comparison
    actual_result = {
        'queries': [
            "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'products' AND COLUMN_NAME IN ('Images 1', 'Images 2', 'Images 3', 'Images 4');",
            "SELECT row_number() over (order by (select null)) as row_num, * FROM products WHERE `Images 1` IS NULL OR `Images 2` IS NULL OR `Images 3` IS NULL OR `Images 4` IS NULL;"
        ]
    }
    
    # Perform the actual API call
    result = generate_sql_queries(requirement, column_names, openai_client)
    
    # Verify the response structure and content
    assert result['queries'][0].lower() == actual_result['queries'][0].lower(), "First query does not match the expected result"
    # Uncomment the following line if you want to verify the second query as well
    # assert result['queries'][1].lower() == actual_result['queries'][1].lower(), "Second query does not match the expected result"