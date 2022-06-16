"""Module for creating body of email report with scraped cars."""


class MailBuilder:
    """Class for creating report in html format."""

    def __init__(self, cars: list):
        """Create instance using list of dictionaries with scraped cars."""
        self.cars = cars

    def _build_car_message(self, car: dict):
        return f"""\
<div style="display:flex; flex-direction: row; justify-content: left; align-items: left">
  <div>
     <a href={car["url"]}>
     <img src={car["photo_url"]} alt="otomoto.pl"/>
     </a>
  </div>
  <div style="padding-left:10px">
    <p><h2><a href={car["url"]}>{car["name"]}</a></h2></p>
    <p><h3 style="color:Orange;">{car["price"]}</h3> </p>
    <p>Rocznik: <b>{car["year"]}</b></p>
    <p>Przebieg: <b>{car["distance"]}</b></p>
    <p>Silnik: {car["engine_volume"]} <b>{car["fuel"]}</b></p>
    <p>Lokalizacja: <b>{car["location"]}</b></p>
  </div>
</div>
<hr>
"""

    def build_html_report(self):
        """Create full html report, containing every car."""
        return f"""\
<html>
  <head></head>
  <body>
    {''.join(self._build_car_message(car) for car in self.cars)}
  </body>
</html>
"""
