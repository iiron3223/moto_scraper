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

    # Track number of attempts in case of failed scraping
    attempts_limit = 3
    attempts_made = 0
    finished = False

    while not finished and attempts_made < attempts_limit:
        attempts_made += 1

        # Start crawl
        logging.info(f"Starting scraping using motospider (attempt {attempts_made})")
        os.system("scrapy crawl --nolog motospider")

        # Send emails
        mail_sender = MailSender(new_cars_filepath, all_cars_filepath)
        mail_sender.send_email(username, password, recipients)

        finished = bool(mail_sender.all_cars)

    # Log end of task
    if finished:
        logging.info("Job completed")
    else:
        logging.warning("Scraping failed")
