import logging
import os

import scrapy
from dotenv import load_dotenv
from scrapy.utils.project import data_path

from mailer.mailer import MailSender


def load_recipients(path):
    """Load list of recipient email addresses."""
    with open(path) as f:
        return f.read().strip().split("\n")


if __name__ == "__main__":
    load_dotenv()
    username = os.getenv("SENDER")
    password = os.getenv("SENDER_PASS")
    new_cars_filepath = data_path("new_cars.json")
    all_cars_filepath = data_path("all_cars.json")
    recipients_filepath = data_path("recipients.txt")
    recipients = load_recipients(recipients_filepath)

    os.system("scrapy crawl --nolog motospider")

    mail_sender = MailSender(new_cars_filepath, all_cars_filepath)
    mail_sender.send_email(username, password, recipients)
