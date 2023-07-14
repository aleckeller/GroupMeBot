import openai
import os

def get_response(content: str) -> str:
    # Set the API key
    openai.api_key = os.environ.get("OPEN_AI_KEY")

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": content}
        ]
    )

    return completion.choices[0].message.content