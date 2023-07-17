import scrapy
from ..items import SrcDexItem

class IndicesInfoSpider(scrapy.Spider):
    name = "indicesinfo"
    start_urls = [
        "https://www.investing.com/indices/us-30", 
        "https://www.investing.com/indices/us-spx-500",
        "https://www.investing.com/indices/nasdaq-composite",
        "https://www.investing.com/indices/volatility-s-p-500",
        "https://www.investing.com/indices/smallcap-2000",
        "https://www.investing.com/indices/kospi",
        "https://www.investing.com/indices/kosdaq",
        "https://www.investing.com/crypto/bitcoin/btc-usd",
        "https://www.investing.com/crypto/ethereum/eth-usd",
        "https://www.investing.com/currencies/usd-krw",
        "https://www.investing.com/currencies/jpy-krw",
        "https://www.investing.com/etfs/spdr-s-p-500",
        "https://www.investing.com/etfs/ultrapro-short-qqq",
        "https://www.investing.com/etfs/powershares-qqqq",
        "https://www.investing.com/etfs/ishares-russell-2000-index-etf",
        "https://www.investing.com/etfs/ishares-ftse-xinhua-china-25",
        "https://www.investing.com/commodities/gold",
        "https://www.investing.com/commodities/brent-oil",
        "https://www.investing.com/commodities/crude-oil",
        "https://www.investing.com/commodities/copper",
        "https://www.investing.com/commodities/us-corn",
        "https://www.investing.com/commodities/natural-gas",
        "https://www.investing.com/rates-bonds/u.s.-2-year-bond-yield",
        "https://www.investing.com/rates-bonds/u.s.-10-year-bond-yield",
        "https://www.investing.com/etfs/samsung-kodex-kospi-200-securities",
        "https://www.investing.com/etfs/samsung-kodex-200-total-return",
        "https://www.investing.com/etfs/samsung-kodex-leverage",
        "https://www.investing.com/etfs/miraeasset-tiger-kospi-200",
        "https://www.investing.com/etfs/305540",
    ]

    def parse(self, response):
        if ("crypto" in response.url) or ("currencies" in response.url):
            title = response.xpath('//*[@id="__next"]/div[2]/div/div/div[2]/main/div/div[1]/div[1]/h1/text()').get()
            closing = response.xpath('//*[@id="__next"]/div[2]/div/div/div[2]/main/div/div[1]/div[2]/div[1]/span/text()').get()
        elif ("etfs" in response.url):
            title = response.xpath('//*[@id="__next"]/div[2]/div[2]/div/div[1]/div/div[1]/div[1]/div[1]/h1/text()').get()
            closing = response.xpath('//*[@id="__next"]/div[2]/div[2]/div/div[1]/div/div[1]/div[3]/div[1]/div[1]/div[1]/text()').get()
        else: # commodities, indices, bonds
            title = response.xpath('//*[@id="__next"]/div[2]/div[2]/div/div[1]/div/div[1]/div[1]/div[1]/h1/text()').get()
            closing = response.xpath('//*[@id="__next"]/div[2]/div[2]/div/div[1]/div/div[1]/div[3]/div/div[1]/div[1]/text()').get()

        yield SrcDexItem(title=title, closing=closing, url=response.url)      # add url=response.url when you want to update url

class IndexHistorySpider(scrapy.Spider):
    name = "indexhistory"
    
    def start_requests(self):
        yield scrapy.Request(f"{self.URL}-historical-data", self.parse)

    def parse(self, response):
        if ("crypto" in response.url) or ("currencies" in response.url):
            title = response.xpath('//*[@id="__next"]/div[2]/div/div/div[2]/main/div/div[1]/div[1]/h1/text()').get()
            data = response.xpath('//*[@id="__next"]/div[2]/div/div/div[2]/main/div/div[4]/div/div[1]/div/div[3]/div/table/tbody//tr')
        elif ("etfs" in response.url):
            title = response.xpath('//*[@id="__next"]/div[2]/div/div/div[2]/main/div/div[1]/div[1]/h1/text()').get()
            data = response.xpath('//*[@id="__next"]/div[2]/div/div/div[2]/main/div/div[4]/div/div/div[3]/div/table/tbody//tr')
        else:
            title = response.xpath('//*[@id="__next"]/div[2]/div/div/div[2]/main/div/div[1]/div[1]/h1/text()').get()
            data = response.xpath('//*[@id="__next"]/div[2]/div/div/div[2]/main/div/div[4]/div/div/div[3]/div/table/tbody//tr')
        
        values = dict()
        for row in data:
            date = row.xpath('td[1]/time//text()').get()
            price = row.xpath('td[2]//text()').get()
            values[date] = price
        yield SrcDexItem(title=title, values=values)