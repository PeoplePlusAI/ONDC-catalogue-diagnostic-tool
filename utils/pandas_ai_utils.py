from llama_index.query_pipeline import (
    QueryPipeline as QP,
    Link,
    InputComponent
)
from llama_index.query_engine.pandas import PandasInstructionParser
from llama_index.llms import OpenAI
from llama_index.prompts import PromptTemplate
from dotenv import load_dotenv
import json
import os

load_dotenv(
    dotenv_path='ops/.env',
)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
print(OPENAI_API_KEY)


def create_pandas_prompt(df):
    pandas_prompt_str = (
        "You are working with a pandas dataframe in Python.\n"
        "The name of the dataframe is `df`.\n"
        "This is the result of `print(df.head())`:\n"
        "{df_str}\n\n"
        "Follow these instructions:\n"
        "{instruction_str}\n"
        "Query: {query_str}\n\n"
        "Expression:"
    )
    instruction_str = (
        "1. Convert the query to executable Python code using Pandas, including a preliminary check to ensure all columns required for the query are present in the dataframe. Use `df.columns.isin(['required_column1', 'required_column2']).all()` to verify presence.\n"
        "2. If any required column is missing, the code should print a message indicating the missing columns. This step ensures the code does not attempt to execute a query with non-existent columns.\n"
        "3. Assuming all required columns are present, proceed to formulate the query using Pandas.\n"
        "4. The final line of code should be a Python expression suitable for execution with the `eval()` function, representing the query's solution.\n"
        "5. PRINT ONLY THE EXPRESSION or the message about missing columns.\n"
        "6. Do not quote the expression or the missing columns message.\n"
    )
    return PromptTemplate(pandas_prompt_str).partial_format(
        instruction_str=instruction_str, df_str=df.head(5)
    )

def create_output_parser(df):
    return PandasInstructionParser(df)

def create_openai_client(model_name="gpt-4"):
    return OpenAI(model_name,
                  api_key=OPENAI_API_KEY,
                  )

def create_response_synthesis_prompt():
    response_synthesis_prompt_str = (
        "Given an input question, synthesize a response from the query results in a structured JSON string format.\n"
        "Query: {query_str}\n\n"
        "Pandas Instructions (optional):\n{pandas_instructions}\n\n"
        "Pandas Output: {pandas_output}\n\n"
        "Response: Generate a JSON response that includes:\n"
        "- A `pass` key indicating if any rows meet the condition (true or false).\n"
    )
    return PromptTemplate(response_synthesis_prompt_str)

def create_query_pipeline(df):
    llm = create_openai_client()
    pandas_prompt = create_pandas_prompt(df)
    pandas_output_parser = create_output_parser(df)
    response_synthesis_prompt = create_response_synthesis_prompt()
    qp = QP(
        modules={
            "input": InputComponent(),
            "pandas_prompt": pandas_prompt,
            "llm1": llm,
            "pandas_output_parser": pandas_output_parser,
            "response_synthesis_prompt": response_synthesis_prompt,
            "llm2": llm,
        },
        verbose=True,
    )
    qp.add_chain(
        [
            "input", 
            "pandas_prompt",
            "llm1",
            "pandas_output_parser",
        ]
    )
    qp.add_links(
        [
            Link("input", "response_synthesis_prompt", dest_key="query_str"),
            Link("llm1", "response_synthesis_prompt", dest_key="pandas_instructions"),
            Link("pandas_output_parser", "response_synthesis_prompt", dest_key="pandas_output"), 
        ]
    )
    qp.add_link("response_synthesis_prompt", "llm2")
    return qp


def get_response(df, queries):
    responses = []
    for query in queries:
        qp = create_query_pipeline(df)
        response =  qp.run(query_str=query)
        responses.append(json.loads(response.message.content))
    return responses