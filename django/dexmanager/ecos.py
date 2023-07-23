import requests

idx_100_url = "http://ecos.bok.or.kr/api/KeyStatisticList/1AJBYOG5GZJC0OMYBOSO/json/kr/1/10"
dict_url = "http://ecos.bok.or.kr/api/StatisticWord/1AJBYOG5GZJC0OMYBOSO/json/kr/1/10/소비자동향지수"
item_spec_url = "http://ecos.bok.or.kr/api/StatisticItemList/1AJBYOG5GZJC0OMYBOSO/json/kr/1/10/601Y002"
history_url = "http://ecos.bok.or.kr/api/StatisticSearch/1AJBYOG5GZJC0OMYBOSO/xml/kr/1/10/901Y009/A/2015/2021/"

response = requests.get(history_url)

# Check the status code of the response
if response.status_code == 200:
    # If the request was successful, print the data
    print(response.json())
else:
    # If the request was unsuccessful, print an error message
    print(f"Request failed with status code {response.status_code}")