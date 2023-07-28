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
    
reduced_title_dict = {
    "한국은행 기준금리 및 여수신금리/한국은행 기준금리": "한국은행 기준금리",
    "시장금리(일별)/콜금리(1일, 전체거래)": "콜금리",
    "시장금리(일별)/국고채(3년)": "국고채(3년)",
    "시장금리(일별)/국고채(5년)": "국고채(5년)",
    "시장금리(일별)/국고채(10년)": "국고채(10년)",
    "시장금리(일별)/회사채(3년, AA-)": "회사채(3년, AA-)",
    "예금은행 수신금리(신규취급액 기준)/저축성수신": "저축성 수신금리",
    "예금은행 대출금리(신규취급액 기준)/대출평균": "대출평균금리",
    "예금은행 총수신(말잔)/원화예금": "예금은행 원화예금",
    "예금은행 대출금(말잔)/총대출금": "예금은행 총대출금",
    "가계신용(업권별, 분기)/가계신용": "가계신용",
    "은행대출금 연체율/가계대출/은행전체 1)": "은행대출금 연체율",
    "M1 상품별 구성내역(평잔, 원계열)/M1(평잔, 원계열)": "협의통화량(M1)",
    "Lf 상품별 구성내역(평잔, 원계열)/Lf(금융기관유동성) : 상품별(평잔,원계열)" : "금융기관 유동성(Lf)", #
    "L(광의유동성) 구성내역(말잔, 원계열)/L (광의 유동성)": "광의유동성(L)",
    "채권거래/전체/거래대금": "채권거래대금",
    "주요 국공채 발행액/잔액/국고채권/발행액": "국고채권 발행액",
    "국제 주요국 경제성장률/한국": "한국 연간 경제성장률",
    "국제 주요국 경제성장률/중국": "중국 연간 경제성장률",
    "국제 주요국 경제성장률/프랑스": "프랑스 연간 경제성장률",
    "국제 주요국 경제성장률/독일": "독일 연간 경제성장률",
    "국제 주요국 경제성장률/일본": "일본 연간 경제성장률",
    "국제 주요국 경제성장률/러시아": "러시아 연간 경제성장률",
    "국제 주요국 경제성장률/영국": "영국 연간 경제성장률",
    "국제 주요국 경제성장률/미국": "미국 연간 경제성장률",
    "주요지표(분기지표)/민간소비": "민간소비",
    "주요지표(분기지표)/설비투자": "설비투자",
    "주요지표(분기지표)/건설투자": "건설투자",
    "주요지표(분기지표)/재화수출": "재화수출",
    "주요지표(연간지표)/1인당 국내총생산(명목, 달러표시)": "1인당 국내총생산(명목)",
    "주요지표(분기지표)/총저축률": "총저축률",
    "주요지표(분기지표)/국내총투자율": "국내총투자율",
    "주요지표(분기지표)/수출입의 대 GNI 비율(명목, 계절조정)": "수출입/GNI 비율(명목)",
    "전산업생산지수(농림어업제외)/전산업생산지수(농림어업 제외)/계절조정": "전산업생산지수(농림어업제외)",
    "산업별 생산/출하/재고 지수/제조업/생산지수(계절조정)": "제조업 생산지수",
    "산업별 생산/출하/재고 지수/제조업/생산자제품 출하지수(계절조정)": "생산자제품 출하지수",
    "산업별 생산/출하/재고 지수/제조업/생산자제품 재고지수(계절조정)": "생산자제품 재고지수",
    "제조업 생산능력 및 가동률 지수/제조업/가동률지수(계절조정)": "제조업 가동률지수",
    "산업별 서비스업생산지수/총지수/계절조정지수": "서비스업생산지수",
    "재별 및 상품군별 판매액지수/총지수/계절조정지수": "판매액 총지수",
    "신용카드/개인 이용금액/합계" :"신용카드 이용금액",
    "재별 및 상품군별 판매액지수/승용차/계절조정지수": "승용차 판매액지수",
    "설비투자지수/계절조정지수": "설비투자지수",
    "설비용 기계류 생산지수/기계설비류(선박제외)/내수출하지수(계절조정)": "기계설비류 내수출하지수",
    "기계수주액/국내수요(선박제외)": "기계수주액",
    "건설기성액/총기성액/불변_계절조정": "건설기성액",
    "건축허가현황/구조별/연면적" :"건축허가현황 연면적",
    "국내건설수주액/총수주액": "국내건설수주액",
    "건축착공현황/연면적/자재별": "건축착공현황",
    "경기종합지수/동행지수순환변동치": "경기종합지수(동행)",
    "경기종합지수/선행지수순환변동치": "경기종합지수(선행)",
    "소비자동향조사(전국, 월, 2008.9~)/소비자심리지수/전체": "소비자심리지수",
    "기업경기실사지수(실적)/제 조 업/업황실적1)": "기업경기실사지수",
    "경제심리지수/경제심리지수(원계열)": "경제심리지수",
    "기업경영분석지표(2009~,전수조사)/제조업/매출액증가율": "제조업 매출액증가율",
    "기업경영분석지표(2009~,전수조사)/제조업/매출액세전순이익률": "제조업 세전순이익률",
    "기업경영분석지표(2009~,전수조사)/제조업/부채비율": "제조업 부채비율",
    "가구당 월평균 가계수지(전국, 2인이상)/명목/소득": "가구당 월평균 가계수지(소득)",
    "가구당 월평균 가계수지(전국, 2인이상)/명목/평균소비성향": "가구당 월평균 가계수지(평균소비성향)",
    "소득분배지표/처분가능소득/지니계수": "지니계수",
    "소득분배지표/처분가능소득/5분위배율": "소득분배 5분위배율",
    "경제활동인구/실업률/원계열": "실업률",
    "경제활동인구/고용률/원계열": "고용률",
    "경제활동인구/경제활동인구/원계열": "경제활동인구",
    "경제활동인구/취업자/원계열": "취업자",
    "시간당 명목임금지수/ALL 비농전산업": "명목임금지수(비농전산업)",
    "노동생산성지수/산업생산기준/광공업(전기,가스,수도업 포함)": "광공업 노동생산성지수",
    "단위노동비용지수/제조업": "제조업 단위노동비용지수",
    "추계인구/고령인구비율/합계출산율/추계인구": "추계인구",
    "추계인구/고령인구비율/합계출산율/고령인구비율(65세 이상)": "고령인구비율(65세 이상)",
    "추계인구/고령인구비율/합계출산율/합계출산율": "합계출산율",
    "경상수지(계절조정)/경상수지": "경상수지",
    "국제수지/직접투자(자산)": "국제수지-직접투자(자산)",
    "국제수지/직접투자(부채)": "국제수지-직접투자(부채)",
    "국제수지/증권투자(자산)": "국제수지-증권투자(자산)",
    "국제수지/증권투자(부채)": "국제수지-증권투자(부채)",
    "수출금액지수/총지수": "수출금액지수",
    "수입금액지수/총지수": "수입금액지수",
    "교역조건지수/순상품교역조건지수": "순상품교역조건지수",
    "교역조건지수/소득교역조건지수": "소득교역조건지수",
    "외환보유액/합계": "외환보유액",
    "대외채무/대외채무": "대외채무",
    "대외채권/대외채권": "대외채권",
    "소비자물가지수/총지수": "소비자물가지수(총지수)",
    "소비자물가지수(특수분류)/농산물및석유류제외지수": "소비자물가지수(농산물및석유류제외)",
    "소비자물가지수(특수분류)/생활물가지수": "소비자물가지수(생활물가지수)",
    "생산자물가지수(기본분류)/총지수": "생산자물가지수",
    "수출물가지수(기본분류)/총지수/원화기준": "수출물가지수",
    "수입물가지수(기본분류)/총지수/원화기준": "수입물가지수",
    "주택매매가격지수(KB)/아파트(서울)": "주택매매가격지수(아파트, 서울)",
    "주택전세가격지수(KB)/아파트(서울)": "주택전세가격지수(아파트, 서울)",
    "지역별 지가변동률/전국": "지가변동률(전국)",
}

def reduce_title(title):
    if title in reduced_title_dict:
        return reduced_title_dict[title]
    else:
        return title

if __name__ == "__main__":
    print(summarize_with_langchain())
    # print(generate_summary())