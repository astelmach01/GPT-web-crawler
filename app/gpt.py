from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def pretty_print(obj):
    d = json.loads(obj)
    print(json.dumps(d, indent=4))


def upload_file(path: str, purpose: str = "assistants"):
    with open(path, "rb") as f:
        return client.files.create(file=f, purpose=purpose)


# see for kwargs https://platform.openai.com/docs/api-reference/assistants/createAssistant
def create_assistant(model: str = "gpt-3.5-turbo-1106", **kwargs):
    args = {"model": model}
    args.update(kwargs)

    return client.beta.assistants.create(**args)


if __name__ == "__main__":
    file_info = upload_file(
        "/Users/andrewstelmach/Desktop/GPT-web-crawler/output/astelmach01_github_io/astelmach01_github_io_master_combined.txt"
    )

    assistant = create_assistant(
        name="astelmach01_github_io docs",
        description="An assistant that can answer questions about my personal website, astelmach01.github.io.",
        file_ids=[file_info.id],
        tools=[{"type": "retrieval"}],
        instructions="You have been provided all the scraped text from a website. Answer questions about the website and give examples where applicable",
    )

    pretty_print(assistant)
