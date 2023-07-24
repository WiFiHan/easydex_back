import openai
from pathlib import Path
import os, environ

env = environ.Env(
    DEBUG=(bool, True)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
env = environ.Env(
    DEBUG=(bool, True)
)
environ.Env.read_env(
    env_file=os.path.join(BASE_DIR, '.env')
)
openai.api_key = env('OPENAI_API_KEY')

def get_completion(prompt, model="gpt-3.5-turbo", temperature=0):
    messages = [{"role": "system", "content": "You are a financial AI assistant."}]
    # Change the system message content to set the role as "system"

    messages.append({"role": "user", "content": prompt})
    # Append the user message to the messages list

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message["content"]

def generate_description(dex):
    prompt = f"""
    You are a financial AI assistant that provides easy explanations of {dex} indicators and recent news for beginners.

    Please provide a simple and concise explanation (around 80 characters) of what {dex} indicator is in Korean.
    """
    response = get_completion(prompt)
    print(response)
    return response

def generate_keywords(dex):
    prompt = f"""
    You are a concise translater that provides easy Korean word of complicated name - {dex} indicator.

    Please provide 5 abbreviations or acronyms that users would search for when they want to know about {dex} indicator.
    Do not add extra explanation. Just provide the keywords.
    If there is no abbreviation or acronym, just provide its short name or full name.
    """
    response = get_completion(prompt)
    return response