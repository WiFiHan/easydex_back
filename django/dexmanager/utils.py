import openai
from pathlib import Path
import os, environ

env = environ.Env(
    DEBUG=(bool, True)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
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
        max_tokens=512,
    )
    return response.choices[0].message["content"]

def generate_summary(title_list):
    prompt = f"""
    You are a financial AI assistant that provides recent topic of investing news for Korean.

    Here each line is the latest economic news titles:\n{title_list}\n
    Please pick 5 important keywords affecting the stock market which appear most frequently and provide it with explanation obeying following features.
    - Each keywords should be less than 3 tokens.
    - Exclude propositional particles and political keywords.
    - The explanation for each keywords could be just one sentence in korean and remove english.
    - 
    """
    response = get_completion(prompt)
    return response

if __name__ == "__main__":
    pass