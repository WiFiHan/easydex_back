import re
import openai
from pathlib import Path
import os, environ

env = environ.Env(
    DEBUG=(bool, True)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
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
    return response

def generate_keywords(dex):
    prompt = f"""
    You are a helper bot that enables searching for investing indiciators with complicated name.

    Please provide 5 abbreviations or acronyms that people would search for when they want to know about {dex} indicator.
    If possible, please provide friendly names in Korean.
    Do not include any explanation.
    """
    response = get_completion(prompt)
    return response

def remove_brackets_and_append(source_list):
    result_list = []
    pattern = r'\((.*?)\)'  # Regular expression pattern to match text inside parentheses

    for item in source_list:
        # Remove brackets and extract elements inside them using re.findall()
        elements_inside_brackets = re.findall(pattern, item)

        # Remove the brackets from the original string
        cleaned_item = re.sub(pattern, '', item).strip()

        # Append the cleaned item to the result_list
        result_list.append(cleaned_item)

        # Append elements inside brackets to the result_list
        result_list.extend(elements_inside_brackets)

    # Remove duplicated elements by converting the list to a set and then back to a list
    result_list = list(set(result_list))

    return result_list
