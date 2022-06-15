import json
import smtplib
from email.headerregistry import Address
from email.message import EmailMessage
from email.utils import make_msgid

from body import MailBuilder

car = None
car_count = 1


class MailSender:
    def __init__(self, car_filepath):
        self.car_filepath = car_filepath
        self.cars = self._load_cars()
        mail_builder = MailBuilder(self.cars)
        self.msg_body = mail_builder.build_email_message()

    def _load_cars(self):
        with open(self.car_filepath) as car_file:
            cars = json.load(car_file)
        return cars

    def send_email(self):
        msg = EmailMessage()
        msg["Subject"] = f"{car_count} owe ogłoszenia na otomoto.pl"
        msg["From"] = Address("OtomotoScraper", "veryhumblebee", "gmail.com")
        msg["To"] = Address("D", "scraper.ortolan", "@8alias.com")
        msg.add_header("Content-Type", "text/html")
        msg.set_payload(self.msg_body)
        print(msg)


if __name__ == "__main__":
    x = MailSender("/home/dominik/python/otomoto/otomoto/.scrapy/new_cars.json")
    x.send_email()
