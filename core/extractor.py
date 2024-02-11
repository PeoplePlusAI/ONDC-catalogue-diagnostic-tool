from utils.instructor_utils import run_instructor
from pydantic import BaseModel
from typing import List
from openai import OpenAI
from enum import Enum


COLUMN_CLASSIFIER_PROMPT = "Classify the following requirement to strongly related column names: "


def create_model(column_names: List[str]):
    column_dict = {
        x: x for x in column_names
    }
    Columns = Enum('Columns', column_dict)
    class MultiClassPrediction(BaseModel):
        """
        Class for a multi-class label prediction
        """

        related_columns: List[Columns]

    return MultiClassPrediction

def compose_prompt(requirement: str):
    return f"{COLUMN_CLASSIFIER_PROMPT} {requirement}."


def extract_columns(requirement: str, client: OpenAI, class_model: BaseModel, model:str = "gpt-4"):
    """
    Extracts the columns from the requirement
    """
    requirement_prompt = compose_prompt(requirement)
    return run_instructor(requirement_prompt, client, class_model, model)