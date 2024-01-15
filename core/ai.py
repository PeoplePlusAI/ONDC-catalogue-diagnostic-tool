from dotenv import load_dotenv
from utils.file_utils import xlsx_to_csv
from openai import OpenAI
import os

load_dotenv(
    dotenv_path='ops/.env',
)

client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
)

def upload_file_to_openai(csv_file_path):
    file = client.files.create(
        file=open(csv_file_path, 'rb'),
        purpose='assistants'
    )
    return file.id

def create_assistant(file_id):
    assistant = client.beta.assistants.create(
        instructions="You are a data analyst assistant when given a requirement and a csv file analyse the csv file and answer if the requirement is satisfied.",
        model="gpt-4-1106-preview",
        tools=[{"type": "code_interpreter"}],
        file_ids=[file_id]
    )
    return assistant.id


def create_thread(requirements, file_id):
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": f"This is the requirement. {requirements}", 
                "file_ids": [file_id]
            }
        ]
    )
    return thread.id

def create_run(assistant_id, thread_id):
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )
    return run.id

def retrieve_run_status(run_id, thread_id):
    run = client.beta.threads.runs.retrieve(
        run_id=run_id,
        thread_id=thread_id
    )
    return run.status

def retrieve_run_messages(thread_id):
    messages = client.beta.threads.messages.list(
        thread_id=thread_id
    )
    message = messages.data[0].content[0].text.value
    return message


def main_logic(csv_file_path, requirements):
    csv_file_path = xlsx_to_csv(csv_file_path)
    file_id = upload_file_to_openai(csv_file_path)
    assistant_id = create_assistant(file_id)
    thread_id = create_thread(requirements, file_id)
    run_id = create_run(assistant_id, thread_id)
    status = retrieve_run_status(run_id, thread_id)
    while status != 'completed':
        status = retrieve_run_status(run_id, thread_id)
    message = retrieve_run_messages(thread_id)
    return message




