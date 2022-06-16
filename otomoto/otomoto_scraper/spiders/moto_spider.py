import logging

import scrapy
from otomoto_scraper.itemloaders import CarItemLoader
from otomoto_scraper.items import CarItem
from scrapy.utils.project import data_path


def get_starting_url():
    """Read starting url from file."""
    url_filepath = data_path("target_url.txt")
    with open(url_filepath) as f:
        url = f.read()
    return url


class MotoSpider(scrapy.Spider):
    name = "motospider"
    allowed_domains = ["otomoto.pl"]
    url = get_starting_url()
    start_urls = [url]
    page_num = 1

    def parse(self, response):
        listings = response.xpath('//article[@data-testid="listing-ad"]')
        for listing in listings:
            # Get additional info about car
            car_info = listing.css("ul").css("li::text").getall()
            if car_info[0] == "Niski przebieg":
                car_info = car_info[1:5]
            else:
                car_info = car_info[0:4]

            # Create car item and scrape all data
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

        # Follow to the next page
        try:
            last_page = response.xpath('//li[@title="Next Page"]').attrib[
                "aria-disabled"
            ]
        except KeyError:
            logging.error("Cannot find next page ('aria-disabled' not found)")
            last_page = "true"

        if last_page == "false":
            self.page_num += 1
            next_page = f"{self.url}&page={self.page_num}"
            yield scrapy.Request(next_page, callback=self.parse)
