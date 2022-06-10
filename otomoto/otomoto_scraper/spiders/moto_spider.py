import scrapy
from scrapy.loader import ItemLoader


class MotoSpider(scrapy.Spider):
    name = "moto_spider"
    allowed_domains = ["otomoto.pl"]
    start_urls = [
        "https://www.otomoto.pl/osobowe/seg-cabrio--seg-city-car--seg-combi--seg-compact--seg-coupe--seg-mini--seg-minivan--seg-suv/kielce?search%5Bfilter_enum_fuel_type%5D=petrol&search%5Bdist%5D=25&search%5Bfilter_float_mileage%3Ato%5D=250000&search%5Bfilter_float_price%3Afrom%5D=10000&search%5Bfilter_float_price%3Ato%5D=20000&search%5Badvanced_search_expanded%5D=true"
    ]

    def parse(self, response):
        articles = response.xpath('//article[@data-testid="listing-ad"]')

        for article in articles:
            # fmt: off
            info = article.css('ul').css('li::text').getall()[:4]
            yield{

                  'name': article.xpath('.//h2//a/text()').get(),
                  'id': article.attrib['id'],
                  'url': article.xpath('.//h2//a').attrib['href'],
                  'price': article.css('span::text').get(),
                  'year': info[0],
                  'distance': info[1],
                  'engine_volume': info[2],
                  'fuel': info[3],
                  'photo_url': article.css('img').attrib['src'],
            }
            # fmt: on
