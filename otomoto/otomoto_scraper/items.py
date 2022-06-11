import scrapy


class CarItem(scrapy.Item):
    name = scrapy.Field()
    id = scrapy.Field()
    price = scrapy.Field()
    year = scrapy.Field()
    distance = scrapy.Field()
    engine_volume = scrapy.Field()
    fuel = scrapy.Field()
    location = scrapy.Field()
    url = scrapy.Field()
    photo_url = scrapy.Field()
