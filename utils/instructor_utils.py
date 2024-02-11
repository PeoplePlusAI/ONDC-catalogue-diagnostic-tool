import json
import instructor
from pydantic import BaseModel
from openai import OpenAI

def patch_client(client: OpenAI):
    """
    Patch the client with the instructor
    """
    return instructor.patch(client)

def run_instructor(requirement_prompt: str, client: OpenAI, class_model: BaseModel, model:str = "gpt-4"):
    """
    Extracts the columns from the requirement
    """
    response = client.chat.completions.create(
        model=model,
        response_model=class_model,
        messages=[
            {
                "role": "user",
                "content": requirement_prompt,
            },
        ],
    )
    return json.loads(response.model_dump_json())