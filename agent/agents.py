from openai import OpenAI
from pydantic import BaseModel
from typing import Type
from config.config import OPEN_AI_KEY

client = OpenAI(api_key=OPEN_AI_KEY)

def custom_agent(
    system_prompt: str,
    user_query: str,
    response_model: Type[BaseModel],
    model_name: str = "gpt-4o-2024-08-06",
):
    """
    Sends a prompt and user query to OpenAI, parses the response with a Pydantic model.

    Args:
        system_prompt (str): The system message prompt.
        user_query (str): The user message/query.
        response_model (Type[BaseModel]): Pydantic model class to parse the output.
        model_name (str): OpenAI model to use. Defaults to 'gpt-4o-2024-08-06'.

    Returns:
        An instance of the response_model parsed from the output.
    """
    response = client.responses.parse(
        model=model_name,
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query},
        ],
        text_format=response_model,
    )
    return response.output_parsed
