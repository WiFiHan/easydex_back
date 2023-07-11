import scrapy
from scraper.items import IndexItem

class CrawlerSpider(scrapy.Spider):
    name = "crawler"
    allowed_domains = ["investing.com"]
    start_urls = [
        "https://www.investing.com/indices/us-30", 
        "https://www.investing.com/indices/us-spx-500",
        "https://www.investing.com/indices/nasdaq-composite",
        "https://www.investing.com/indices/volatility-s-p-500",
        "https://www.investing.com/indices/smallcap-2000",
        "https://www.investing.com/indices/kospi",
        "https://www.investing.com/indices/kosdaq",
    ]

    def parse(self, response):
        name = response.xpath('//*[@id="__next"]/div[2]/div[2]/div/div[1]/div/div[1]/div[1]/div[1]/h1/text()').get()
        closing = response.xpath('//*[@id="__next"]/div[2]/div[2]/div/div[1]/div/div[1]/div[3]/div/div[1]/div[1]/text()').get()
        print('title :', name)
        print('closing :', closing)
        yield IndexItem(name=name, closing=closing)