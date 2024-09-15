import os
from dotenv import load_dotenv
import chainlit as cl
from langsmith import traceable
from langsmith.wrappers import wrap_openai
import openai
import asyncio
import json
from datetime import datetime
from prompts import ASSESSMENT_PROMPT, SYSTEM_PROMPT, CLASS_CONTEXT
from user_record import read_user_record, write_user_record, format_user_record, parse_user_record

# Load environment variables
load_dotenv(override=True)

configurations = {
    "openai_gpt-4": {
        "endpoint_url": os.getenv("OPENAI_ENDPOINT"),
        "api_key": os.getenv("OPENAI_API_KEY"),
        "model": "gpt-4"
    }
}

# Choose configuration
config_key = "openai_gpt-4"

# Get selected configuration
config = configurations[config_key]

# Initialize the OpenAI async client
client = wrap_openai(openai.AsyncClient(api_key=config["api_key"], base_url=config["endpoint_url"]))

gen_kwargs = {
    "model": config["model"],
    "temperature": 0.3,
    "max_tokens": 500
}

# Configuration setting to enable or disable the system prompt
ENABLE_SYSTEM_PROMPT = True
ENABLE_CLASS_CONTEXT = True

def get_latest_user_message(message_history):
    # Iterate through the message history in reverse to find the last user message
    for message in reversed(message_history):
        if message['role'] == 'user':
            return message['content']
    return None

@traceable
async def assess_message(message_history):
    file_path = "user_record.md"
    markdown_content = read_user_record(file_path)
    parsed_record = parse_user_record(markdown_content)

    latest_message = get_latest_user_message(message_history)

    # Remove the original prompt from the message history for assessment
    filtered_history = [msg for msg in message_history if msg['role'] != 'system']

    # Convert message history, alerts, and preferences to strings
    history_str = json.dumps(filtered_history, indent=4)
    alerts_str = json.dumps(parsed_record.get("Alerts", []), indent=4)
    preferences_str = json.dumps(parsed_record.get("Preferences", {}), indent=4)
    
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Generate the assessment prompt
    filled_prompt = ASSESSMENT_PROMPT.format(
        latest_message=latest_message,
        history=history_str,
        existing_alerts=alerts_str,
        existing_preferences=preferences_str,
        current_date=current_date
    )
    if ENABLE_CLASS_CONTEXT:
        filled_prompt += "\n" + CLASS_CONTEXT.format(current_date=current_date)
    print("Filled prompt: \n\n", filled_prompt)

    response = await client.chat.completions.create(messages=[{"role": "system", "content": filled_prompt}], **gen_kwargs)

    assessment_output = response.choices[0].message.content.strip()
    print("Assessment Output: \n\n", assessment_output)

    # Parse the assessment output
    new_alerts, preference_updates = parse_assessment_output(assessment_output)

    # Update the user record with the new alerts and preference updates
    parsed_record["Alerts"].extend(new_alerts)
    for update in preference_updates:
        preference = update["preference"]
        note = update["note"]
        parsed_record["Preferences"][preference] = note

    # Format the updated record and write it back to the file
    updated_content = format_user_record(
        parsed_record["User Information"],
        parsed_record["Alerts"],
        parsed_record["Preferences"]
    )
    write_user_record(file_path, updated_content)

def parse_assessment_output(output):
    try:
        parsed_output = json.loads(output)
        new_alerts = parsed_output.get("new_alerts", [])
        preference_updates = parsed_output.get("preference_updates", [])
        return new_alerts, preference_updates
    except json.JSONDecodeError as e:
        print("Failed to parse assessment output:", e)
        return [], []

@cl.on_message
@traceable
async def on_message(message: cl.Message):
    message_history = cl.user_session.get("message_history", [])

    if ENABLE_SYSTEM_PROMPT and (not message_history or message_history[0].get("role") != "system"):
        system_prompt_content = SYSTEM_PROMPT
        if ENABLE_CLASS_CONTEXT:
            current_date = datetime.now().strftime('%Y-%m-%d')
            system_prompt_content += "\n" + CLASS_CONTEXT.format(current_date=current_date)
        message_history.insert(0, {"role": "system", "content": system_prompt_content})

    message_history.append({"role": "user", "content": message.content})

    asyncio.create_task(assess_message(message_history))
    
    response_message = cl.Message(content="")
    await response_message.send()

    stream = await client.chat.completions.create(messages=message_history, stream=True, **gen_kwargs)
    async for part in stream:
        if token := part.choices[0].delta.content or "":
            await response_message.stream_token(token)

    message_history.append({"role": "assistant", "content": response_message.content})
    cl.user_session.set("message_history", message_history)
    await response_message.update()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    cl.run(host="0.0.0.0", port=port)
