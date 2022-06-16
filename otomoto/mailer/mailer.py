"""Module for creating and sending mail reports about scraped cars."""

import json
import logging
import smtplib
import ssl
from email.headerregistry import Address
from email.message import EmailMessage

from mailer.body import MailBuilder


class MailSender:
    """Class for creating and sending emails based on Scrapy report."""

    def __init__(self, new_cars_filepath: str, all_cars_filepath: str):
        """Build body of message and attachment using reports in json format."""
        self.new_cars_filepath = new_cars_filepath
        self.new_cars = self._load_cars(self.new_cars_filepath)
        mail_builder = MailBuilder(self.new_cars)
        self.msg_body = mail_builder.build_html_report()

        self.all_cars_filepath = all_cars_filepath
        self.all_cars = self._load_cars(self.all_cars_filepath)
        attachment_builder = MailBuilder(self.all_cars)
        self.attachment = attachment_builder.build_html_report()

    def _load_cars(self, path: str):
        """Load json car report."""
        with open(path) as car_file:
            cars = json.load(car_file)
        return cars

    def send_email(self, sender_mail: str, password: str, recipients: list):
        """Send email with report about scraped cars."""
        logging.info(f"Number of scraped cars: {len(self.all_cars)}")
        if self.new_cars:
            logging.info(f"{len(self.new_cars)} new cars found")
            msg = EmailMessage()
            msg["From"] = Address("OtomotoScraper")
            msg["Subject"] = self._create_subject()
            msg.add_header("Content-Type", "text/html; charset=utf-8")
            msg.set_payload(self.msg_body)
            msg.add_attachment(
                self.attachment,
                charset="utf-8",
                subtype="html",
                filename="all_cars.html",
            )

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_mail, password)
                server.sendmail(sender_mail, recipients, msg.as_string())
                logging.info(f"Email sent to {recipients}")

            self._clear_new_cars_file()
        else:
            logging.info("No new cars")

    def _clear_new_cars_file(self):
        """Clear data from new car json file."""
        with open(self.new_cars_filepath, "w") as f:
            f.write("[]")

    def _create_subject(self):
        """Create subject for email with proper grammatical form."""
        new_cars_count = len(self.new_cars)
        last_digit = new_cars_count % 10

        if new_cars_count == 1:
            part = "nowe ogłoszenie"
        elif last_digit in (2, 3, 4) and new_cars_count not in (12, 13, 14):
            part = "nowe ogłoszenia"
        else:
            part = "nowych ogłoszeń"
        return f"{len(self.new_cars)} {part} na otomoto.pl"
