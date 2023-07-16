import scrapy
from scraper.items import SrcDexItem

class indicesInfoSpider(scrapy.Spider):
    name = "indicesinfo"
    start_urls = [
        "https://www.investing.com/indices/us-30", 
        "https://www.investing.com/indices/us-spx-500",
        "https://www.investing.com/indices/nasdaq-composite",
        # "https://www.investing.com/indices/volatility-s-p-500",
        # "https://www.investing.com/indices/smallcap-2000",
        # "https://www.investing.com/indices/kospi",
        # "https://www.investing.com/indices/kosdaq",
        # "https://www.investing.com/crypto/bitcoin/btc-usd",
        # "https://www.investing.com/crypto/ethereum/eth-usd",
        # "https://www.investing.com/currencies/usd-krw",
        # "https://www.investing.com/currencies/jpy-krw",
    ]

    def parse(self, response):
        if ("crypto" in response.url) or ("currencies" in response.url):
            title = response.xpath('//*[@id="__next"]/div[2]/div/div/div[2]/main/div/div[1]/div[1]/h1/text()').get()
            closing = response.xpath('//*[@id="__next"]/div[2]/div/div/div[2]/main/div/div[1]/div[2]/div[1]/span/text()').get()
        else:
            title = response.xpath('//*[@id="__next"]/div[2]/div[2]/div/div[1]/div/div[1]/div[1]/div[1]/h1/text()').get()
            closing = response.xpath('//*[@id="__next"]/div[2]/div[2]/div/div[1]/div/div[1]/div[3]/div/div[1]/div[1]/text()').get()

        yield SrcDexItem(title=title, closing=closing)

class IndexHistorySpider(scrapy.Spider):
    name = "indexhistory"
    start_urls = [
        "https://www.investing.com/indices/us-30-historical-data",
        "https://www.investing.com/currencies/usd-krw-historical-data",
    ]

    def parse(self, response):
        if ("crypto" in response.url) or ("currencies" in response.url):
            title = response.xpath('//*[@id="__next"]/div[2]/div/div/div[2]/main/div/div[1]/div[1]/h1/text()').get()
            data = response.xpath('//*[@id="__next"]/div[2]/div/div/div[2]/main/div/div[4]/div/div[1]/div/div[3]/div/table/tbody//tr')
        else:
            title = response.xpath('//*[@id="__next"]/div[2]/div/div/div[2]/main/div/div[1]/div[1]/h1/text()').get()
            data = response.xpath('//*[@id="__next"]/div[2]/div/div/div[2]/main/div/div[4]/div/div/div[3]/div/table/tbody//tr')
        values = dict()
        for row in data:
            date = row.xpath('td[1]/time//text()').get()
            price = row.xpath('td[2]//text()').get()
            values[date] = price
        yield SrcDexItem(title=title, values=values)