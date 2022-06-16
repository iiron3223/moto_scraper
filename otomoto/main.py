"""Main script for managing scraping and sending emails."""

import logging
import os

from dotenv import load_dotenv
from scrapy.utils.project import data_path

from mailer.mailer import MailSender


def load_recipients(path):
    """Load list of recipient email addresses."""
    with open(path) as f:
        return f.read().strip().split("\n")


if __name__ == "__main__":

    # Set up logging
    logging.basicConfig(
        filename="logs.log",
        filemode="a",
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Get credentials
    load_dotenv()
    username = os.getenv("SENDER")
    password = os.getenv("SENDER_PASS")

    # Specify file paths and load data
    new_cars_filepath = data_path("new_cars.json")
    all_cars_filepath = data_path("all_cars.json")
    recipients_filepath = data_path("recipients.txt")
    recipients = load_recipients(recipients_filepath)

    # Start crawl
    logging.info("Starting scraping using motospider")
    os.system("scrapy crawl --nolog motospider")

    # Send emails
    mail_sender = MailSender(new_cars_filepath, all_cars_filepath)
    mail_sender.send_email(username, password, recipients)

    logging.info("Job completed")
