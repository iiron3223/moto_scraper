import scrapy
from scrapy.loader import ItemLoader

URL = "https://www.otomoto.pl/osobowe/seg-city-car--seg-compact/kielce?search%5Bfilter_enum_fuel_type%5D=petrol&search%5Filister_enum_damaged%5D=0&search%5Bfilter_enum_no_accident%5D=1&search%5Bdist%5D=25&search%5Bfilter_float_mileage%3Ato%5D=250000&search%5Bfilter_float_price%3Afrom%5D=10000&search%5Bfilter_float_price%3Ato%5D=20000"


class MotoSpider(scrapy.Spider):
    name = "motospider"
    allowed_domains = ["otomoto.pl"]
    start_urls = [URL]
    page_num = 1

    def parse(self, response):
        listings = response.xpath('//article[@data-testid="listing-ad"]')
        for listing in listings:
            car_info = listing.css("ul").css("li::text").getall()
            if car_info[0] == "Niski przebieg":
                car_info = car_info[1:5]
            else:
                car_info = car_info[0:4]

            yield {
                "name": listing.xpath(".//h2//a/text()").get(),
                "id": listing.attrib["id"],
                "price": listing.css("span::text").get(),
                "year": car_info[0],
                "distance": car_info[1],
                "engine_volume": car_info[2],
                "fuel": car_info[3],
                "location": listing.xpath(".//div/p[svg]/text()").get(),
                "url": listing.xpath(".//h2//a").attrib["href"],
                "photo_url": listing.css("img").attrib["src"],
            }

        last_page = response.xpath('//li[@title="Next Page"]').attrib["aria-disabled"]
        if last_page == "false":
            self.page_num += 1
            next_page = f"{URL}&page={self.page_num}"
            yield scrapy.Request(next_page, callback=self.parse)
