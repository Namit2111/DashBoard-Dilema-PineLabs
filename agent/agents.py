# from openai import OpenAI
# from pydantic import BaseModel
# from typing import Type
# from config.config import OPEN_AI_KEY

# client = OpenAI(api_key=OPEN_AI_KEY)

# def custom_agent(
#     system_prompt: str,
#     user_query: str,
#     response_model: Type[BaseModel],
#     model_name: str = "gpt-4.1",
# ):
#     """
#     Sends a prompt and user query to OpenAI, parses the response with a Pydantic model.

#     Args:
#         system_prompt (str): The system message prompt.
#         user_query (str): The user message/query.
#         response_model (Type[BaseModel]): Pydantic model class to parse the output.
#         model_name (str): OpenAI model to use. Defaults to 'gpt-4o-2024-08-06'.

#     Returns:
#         An instance of the response_model parsed from the output.
#     """
#     response = client.responses.parse(
#         model=model_name,
#         input=[
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": user_query},
#         ],
#         text_format=response_model,
#     )
#     return response.output_parsed



from google import genai
from pydantic import BaseModel
from typing import Type
from config.config import GEMINI_API_KEY  # Replace with your actual key path or value

# Initialize Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)
# model = genai.GenerativeModel(model_name="gemini-2.0-flash-lite")  # You can change the model name as needed

def custom_agent(
    system_prompt: str,
    user_query: str,
    response_model: Type[BaseModel],
    model_name: str = "gemini-2.0-flash-lite",
):
    """
    Sends a system prompt and user query to Gemini, parses the response with a Pydantic model.

    Args:
        system_prompt (str): The system message prompt.
        user_query (str): The user message/query.
        response_model (Type[BaseModel]): Pydantic model class to parse the output.
        model_name (str): Gemini model to use. Defaults to 'gemini-1.5-pro'.

    Returns:
        An instance of the response_model parsed from the output.
    """

    full_prompt = f"{system_prompt}\n\n user query  : {user_query}"

    # Generate content
    response = client.models.generate_content(
        model=model_name, contents=full_prompt,config={
        "response_mime_type": "application/json",
        "response_schema": response_model,
    })

    # Parse response
    return response.parsed  # This will be an instance of the Pydantic model
