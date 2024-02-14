from utils.instructor_utils import run_instructor
from pydantic import BaseModel
from typing import List
from openai import OpenAI

with open("prompts/generate_sql_prompt.txt", "r") as file:
    GENERATE_SQL_PROMPT = file.read()


class SQLQUERYMODEL(BaseModel):
    """
    Class for an SQL QUERY 
    """
    queries: List[str]

class RESPONSEMODEL(BaseModel):
    """
    Class for the response of the SQL query
    """
    passed: bool
    failed_rows: List[int]

def compose_generate_prompt(requirement: str, column_names: str, table_name: str, sql_prompt):
    """
    Compose the prompt for the SQL query
    """
    return sql_prompt.format(requirement=requirement, column_names=column_names, table_name=table_name)


def generate_sql_queries(requirement: str, column_names: str, client: OpenAI, model: str = "gpt-4", sql_prompt=GENERATE_SQL_PROMPT):
    """
    Extracts the columns from the requirement
    """
    requirement_prompt = compose_generate_prompt(requirement, column_names, "products", sql_prompt)
    return run_instructor(requirement_prompt, client, SQLQUERYMODEL, model)

def compose_interpret_prompt(response_1: str, response_2: str):
    """
    Compose the prompt for the interpretation of the SQL query
    """
    return f"Interpret if the requirement passed from the responses {response_1} and {response_2}. If the requirement is not passed, return the row numbers that failed from {response_2}"


def interpret_sql_queries(response_1: str, response_2: str, client: OpenAI, model: str = "gpt-4"):
    """
    Interpret the SQL queries
    """
    interpret_prompt = compose_interpret_prompt(response_1, response_2)
    return run_instructor(interpret_prompt, client, RESPONSEMODEL, model)