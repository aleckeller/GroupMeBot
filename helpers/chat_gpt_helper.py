import openai
import os

def get_response(prompt: str) -> str:
    # Set the API key
    openai.api_key = os.environ.get("OPEN_AI_KEY")

    # Send a request to the API
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response["choices"][0]["text"]