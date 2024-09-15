import openai
from langsmith.wrappers import wrap_openai
from langsmith import traceable
import os
os.environ["LANGCHAIN_API_KEY"] = "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"


# Auto-trace LLM calls in-context
client = wrap_openai(openai.Client())

@traceable # Auto-trace this function
def pipeline(user_input: str):
    result = client.chat.completions.create(
        messages=[{"role": "user", "content": user_input}],
        model="gpt-3.5-turbo"
    )
    return result.choices[0].message.content

pipeline("Hello, world!")
# Out:  Hello there! How can I assist you today?