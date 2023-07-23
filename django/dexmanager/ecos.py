import requests
import ssl

url = "http://ecos.bok.or.kr/api/KeyStatisticList/1AJBYOG5GZJC0OMYBOSO/json/kr/1/10"

response = requests.get(url)

# Check the status code of the response
if response.status_code == 200:
    # If the request was successful, print the data
    print(response.json())
else:
    # If the request was unsuccessful, print an error message
    print(f"Request failed with status code {response.status_code}")