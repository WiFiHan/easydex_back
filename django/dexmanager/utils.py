import openai
from pathlib import Path
import os, environ

from langchain.chat_models import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

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

def summarize_with_langchain():
    loader = TextLoader(file_path='dexmanager/newsdata/contents.txt', encoding='utf-8')
    result = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=3000)
    docs = text_splitter.split_documents(result)
    llm = ChatOpenAI(temperature=0)
    chain = load_summarize_chain(llm, chain_type="map_reduce", verbose=False)
    summary = chain.run(docs)
    return summary

def get_completion(prompt, model="gpt-3.5-turbo", temperature=0):

    messages = [
        {"role": "system", "content": "You are a friendly financial AI assistant."},
                ]
    messages.append({"role": "user", "content": prompt})
    # Append the user message to the messages list

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=1024,
    )
    return response.choices[0].message["content"]

def generate_summary(summary):
    prompt = f"""
    You are a financial AI assistant that provides recent topic of investing news for Korean briefly.
    Here each line is the latest economic news summary:\n{summary}\n

    Read the latest economic news summary above, and then pick only 5 important keywords affecting the stock market. After then, provide it with explanation obeying following features.
    - When you choose a keyword, you shouldn't be biased at the beginning of the text: Read the whole lines.
    - Each keyword must be less than 10 tokens.
    - Each line must include only one keyword.
    - We are not interested in the information which is not related to investment.
    - Include specific trends reflected in the indicators as much as possible.
    - Exclude propositional particles and political keywords.
    - Your answer is better when the explanation is more specific.
    - Your answer must be only in Korean in both keyword and explanation. The keyword and explanation for each keywords could be just one sentence in Korean. You MUST EXCLUDE additional English Explanations.

    """
    response = get_completion(prompt)
    return response

def execute():
    try:
        print("Start summarizing news...")
        summary = summarize_with_langchain()
    except Exception as e:
        print(e, "Error summarizing news.")
    try:
        print("Start generating keywords...")
        keywords = generate_summary(summary)
        return keywords
    except Exception as e:
        print(e, "Error generating keywords.")
        return 

if __name__ == "__main__":
    print(summarize_with_langchain())
    # print(generate_summary())