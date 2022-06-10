import scrapy


class MotoSpiderSpider(scrapy.Spider):
    name = "moto_spider"
    allowed_domains = ["otomoto.pl"]
    start_urls = ["http://www.otomoto.pl/"]

    def parse(self, response):
        pass
