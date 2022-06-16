import json
import os

from itemadapter import ItemAdapter
from scrapy.utils.project import data_path

ids_filename = "car_ids.txt"
ids_data_path = data_path(ids_filename)
new_cars_filename = "new_cars.json"
new_cars_data_path = data_path(new_cars_filename)
all_cars_filename = "all_cars.json"
all_cars_data_path = data_path(all_cars_filename)


class NewCarsPipeline:
    def __init__(self):
        self.new_cars = []
        self.new_ids = []
        self.old_car_ids = {}
        self.all_cars = []

    def open_spider(self, spider):
        # Read ids of cars from previous scrapings
        if os.path.exists(ids_data_path) and os.path.getsize(ids_data_path) > 0:
            with open(ids_data_path, "r") as f:
                content = f.read().strip()[:-1]
                self.old_car_ids = {car_id for car_id in content.split(";")}

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Check if car was already scraped
        # If it is new, save it
        car_id = adapter.get("id")
        car_dict = dict(item)
        if car_id not in self.old_car_ids:
            self.new_cars.append(car_dict)
            self.new_ids.append(car_id)
        self.all_cars.append(car_dict)
        return item

    def close_spider(self, spider):
        # Save ids of cars that were not present during previous scrapings
        if self.new_ids:
            ids_to_write = ";".join(self.new_ids) + ";"
            with open(ids_data_path, "a", encoding="utf8") as f:
                f.write(ids_to_write)

        # Save new cars
        with open(new_cars_data_path, "w", encoding="utf8") as f:
            json.dump(self.new_cars, f, indent=4)

        # Save all cars
        with open(all_cars_data_path, "w", encoding="utf8") as f:
            json.dump(self.all_cars, f, indent=4)
