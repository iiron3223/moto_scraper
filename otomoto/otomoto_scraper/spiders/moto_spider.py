import logging

import scrapy
from otomoto_scraper.itemloaders import CarItemLoader
from otomoto_scraper.items import CarItem
from scrapy.loader import ItemLoader

URL = "https://www.otomoto.pl/osobowe/seg-city-car--seg-compact/kielce?search%5Bfilter_enum_fuel_type%5D=petrol&search%5Bfilter_enum_no_accident%5D=1&search%5Bdist%5D=25&search%5Bfilter_float_mileage%3Ato%5D=250000&search%5Bfilter_float_price%3Afrom%5D=10000&search%5Bfilter_float_price%3Ato%5D=20000&search%5Badvanced_search_expanded%5D=true"


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

            car = CarItemLoader(item=CarItem(), selector=listing)
            car.add_xpath("name", ".//h2//a/text()")
            car.add_value("id", listing.attrib["id"])
            car.add_xpath("price", ".//div/span/text()")
            car.add_value("year", car_info[0])
            car.add_value("distance", car_info[1])
            car.add_value("engine_volume", car_info[2])
            car.add_value("fuel", car_info[3])
            car.add_xpath("location", ".//div/p[svg]/text()")
            car.add_xpath("url", ".//h2//a/@href")
            car.add_value("photo_url", listing.css("img").attrib["src"])

            yield car.load_item()

        try:
            last_page = response.xpath('//li[@title="Next Page"]').attrib[
                "aria-disabled"
            ]
        except KeyError:
            logging.ERROR("Cannot find next page ('aria-disabled' not found)")
            last_page = "true"

        if last_page == "false":
            self.page_num += 1
            next_page = f"{URL}&page={self.page_num}"
            yield scrapy.Request(next_page, callback=self.parse)
