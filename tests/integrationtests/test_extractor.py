import pytest
from openai import OpenAI
from core.extractor import create_model, extract_columns
from utils.instructor_utils import patch_client
from dotenv import load_dotenv
import os

# Assuming your project structure and imports are correct

@pytest.fixture(scope="module")
def openai_client():
    load_dotenv("ops/.env")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    client = patch_client(OpenAI(api_key=OPENAI_API_KEY))
    return client

def test_extract_columns_integration_1(openai_client):
    requirement = "All products should have four image columns"
    column_names = ['Images', 'Images 3', 'Images 4', 'Images 5', 'product_id', 'product_name', 'product_description', 'other_details']
    MultiClassPrediction = create_model(column_names)
    result = extract_columns(requirement, openai_client, MultiClassPrediction)
    assert result['related_columns'] == ['Images', 'Images 3', 'Images 4', 'Images 5']

def test_extract_columns_integration_2(openai_client):
    requirement = "All products should have short description and long description"
    column_names = ['Images', 'Images 3', 'Images 4', 'Images 5', 'product_id', 'product_name', 'product_description', 'other_details']
    MultiClassPrediction = create_model(column_names)
    result = extract_columns(requirement, openai_client, MultiClassPrediction)
    assert result['related_columns'] == ['product_description', 'other_details']

def test_extract_columns_integration_3(openai_client):
    requirement = "All products should have a product_id, product_name, product_description, and other_details"
    column_names = ['Images', 'Images 3', 'Images 4', 'Images 5', 'product_id', 'product_name', 'product_description', 'other_details']
    MultiClassPrediction = create_model(column_names)
    result = extract_columns(requirement, openai_client, MultiClassPrediction)
    assert result['related_columns'] == ["product_id", "product_name", "product_description", "other_details"]

def test_extract_columns_integration_4(openai_client):
    requirement = "product name should have name, pack size and brand name"
    column_names = ['Images', 'Images 3', 'Images 4', 'Images 5', 'product_id', 'product_name', 'product_description', 'other_details']
    MultiClassPrediction = create_model(column_names)
    result = extract_columns(requirement, openai_client, MultiClassPrediction)
    assert result['related_columns'] == ["product_name"]
