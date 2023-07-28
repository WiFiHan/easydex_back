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

reduced_title_dict = {
    "Dow Jones Industrial Average (DJI)": "Dow Jones",
    "S&P 500 (SPX)": "S&P 500",
    "NASDAQ Composite (IXIC)": "NASDAQ",
    "CBOE Volatility Index (VIX)": "VIX",
    "US Small Cap 2000 (RUT)": "US Small Cap 2000",
    "KOSPI (KS11)": "코스피",
    "KOSDAQ (KQ11)": "코스닥",
    "BTC/USD - Bitcoin US Dollar": "비트코인",
    "ETH/USD - Ethereum US Dollar": "이더리움",
    "USD/KRW - US Dollar Korean Won": "달러/원 환율",
    "JPY/KRW - Japanese Yen Korean Won": "엔/원 환율",
    "SPDR® S&P 500 (SPY)": "S&P 500 ETF",
    "ProShares UltraPro Short QQQ (SQQQ)": "Short QQQ ETF",
    "Invesco QQQ Trust (QQQ)": "Invesco QQQ ETF(QQQ)",
    "iShares Russell 2000 ETF (IWM)": "Russell 2000 ETF",
    "iShares China Large-Cap ETF (FXI)": "China Large-Cap ETF",
    "Gold Futures - Aug 23 (GCQ3)": "금 선물",
    "Brent Oil Futures - Oct 23 (LCOV3)": "브렌트유 선물",
    "Crude Oil WTI Futures - Sep 23 (CLU3)": "WTI유 선물",
    "Copper Futures - Sep 23 (HGU3)": "구리 선물",
    "US Corn Futures - Dec 23 (ZCZ3)": "옥수수 선물",
    "Natural Gas Futures - Sep 23 (NGU3)": "천연가스 선물",
    "United States 2-Year Bond Yield": "미국 2년 국채 수익률",
    "United States 10-Year Bond Yield": "미국 10년 국채 수익률",
    "Samsung KODEX 200 ETF (069500)": "KODEX 200 ETF",
    "Samsung KODEX 200 Total Return ETF (278530)": "KODEX 200 TR ETF",
    "Samsung KODEX Leverage ETF[Equity-Derivatives] (122630)": "KODEX 레버리지 ETF",
    "MiraeAsset TIGER 200 ETF (102110)": "TIGER 200 ETF",
    "MiraeAsset TIGER Secondary Cell ETF (305540)": "TIGER 2차전지테마 ETF",
}

def reduce_title(title):
    if title in reduced_title_dict:
        return reduced_title_dict[title]
    else:
        return title