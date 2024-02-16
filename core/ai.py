from utils.file_utils import xlsx_to_csv, load_csv
from core.extractor import extract_columns, create_model
from core.generate_sql import (
    generate_sql_queries
)
from utils.sql_utils import run_sql_queries
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv(
    "ops/.env"
)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def main_logic(csv_file_path, requirement, model):
    column_predictions = extract_columns(requirement, client, model)
    columns_str = ", ".join(column_predictions.get("related_columns"))
    sql_queries = generate_sql_queries(
        requirement, columns_str, client
    )
    queries = sql_queries.get("queries")
    query1, query2 = queries[0], queries[1]
    query_results = run_sql_queries(csv_file_path, query1, query2)
    return query_results
    


def validate_catalogue(csv_file_path, requirements):
    csv_file_path = xlsx_to_csv(csv_file_path)
    df = load_csv(csv_file_path)
    column_names = df.columns
    model = create_model(column_names)
    df.fillna("")
    requirements = requirements.split("\n")
    results = [
        main_logic(
            csv_file_path, requirement, model
        ) for requirement in requirements
    ]
    return results

   



