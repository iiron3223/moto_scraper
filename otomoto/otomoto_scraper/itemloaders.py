from scrapy.loader import ItemLoader

from itemloaders.processors import MapCompose, TakeFirst


class CarItemLoader(ItemLoader):

    default_output_processor = TakeFirst()
    # id_in = MapCompose(int)
    year_in = MapCompose(int)
    # price_in = MapCompose(lambda x: int(str.rstrip(x.replace(" ", ""), "PLN")))
    # distance_in = MapCompose(lambda x: int(str.rstrip(x.replace(" ", ""), "km")))
    # engine_volume_in = MapCompose(lambda x: int(str.rstrip(x.replace(" ", ""), "cm3")))
    fuel_in = MapCompose(str.lower)
    location_in = MapCompose(lambda x: x.split(" ")[:-1])
