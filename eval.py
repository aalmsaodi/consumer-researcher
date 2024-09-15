import openai
from langsmith.wrappers import wrap_openai
from dotenv import load_dotenv

import requests
from bs4 import BeautifulSoup

load_dotenv(override=True)

# Updated URL to the article you want to use
url = "https://www.pcmag.com/lists/best-projectors"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
text = [p.text for p in soup.find_all("p")]
full_text = "\n".join(text)

openai_client = wrap_openai(openai.Client())

def answer_consumer_research_question(inputs: dict) -> dict:
    """
    Generates answers to user questions based on the provided article using OpenAI API.

    Parameters:
    inputs (dict): A dictionary with a single key 'question', representing the user's question as a string.

    Returns:
    dict: A dictionary with a single key 'answer', containing the generated answer as a string.
    """

    # System prompt tailored to consumer research
    system_msg = (
        f"You are a consumer research assistant specializing in projectors. Use the following article to answer the user's question:\n\n{full_text}"
    )

    # Prepare messages
    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": inputs["question"]},
    ]

    # Call OpenAI
    response = openai_client.chat.completions.create(
        messages=messages, model="gpt-3.5-turbo"
    )

    # Response in output dict
    return {"answer": response.dict()["choices"][0]["message"]["content"]}

from langsmith.evaluation import evaluate, LangChainStringEvaluator

# Evaluators
qa_evaluator = [LangChainStringEvaluator("cot_qa")]

# Update the dataset name to your dataset
dataset_name = "research2"

experiment_results = evaluate(
    answer_consumer_research_question,
    data=dataset_name,
    evaluators=qa_evaluator,
    experiment_prefix="test-consumer-research-qa",
    # Any experiment metadata can be specified here
    metadata={
        "variant": "Consumer research assistant with article context",
    },
)