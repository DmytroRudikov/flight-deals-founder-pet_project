import requests
import datetime
from dateutil import relativedelta
import pprint
import os


class FlightSearch:
    def __init__(self):
        self.search_list = []
        self.today = datetime.datetime.today().date()
        self.delta_date = datetime.timedelta(1)
        self.tomorrow = self.today + self.delta_date
        self.delta_months = relativedelta.relativedelta(months=6)
        self.six_months_date = self.tomorrow + self.delta_months
        self.today_formatted = self.today.strftime("%d/%m/%Y")
        self.tomorrow_formatted = self.tomorrow.strftime("%d/%m/%Y")
        self.six_months_date_formatted = self.six_months_date.strftime("%d/%m/%Y")
        self.FLIGHT_SEARCH_ENDPOINT = "https://tequila-api.kiwi.com/v2/search"
        self.KIWI_API_KEY = os.environ.get("KIWI_API_KEY")
        self.kiwi_headers = {
            "apikey": self.KIWI_API_KEY,
        }
        self.kiwi_parameters_no_stopover = {
            "fly_from": "city:LON",
            "date_from": self.tomorrow_formatted,
            "date_to": self.six_months_date_formatted,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "curr": "GBP",
            "max_stopovers": 0,
            "one_for_city": 1,
            "flight_type": "round"
        }
        self.kiwi_parameters_one_stopover = {
            "fly_from": "city:LON",
            "date_from": self.tomorrow_formatted,
            "date_to": self.six_months_date_formatted,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "curr": "GBP",
            "max_stopovers": 1,
            "one_for_city": 1,
            "flight_type": "round"
        }

    def cheapest_flight_search(self, sheets_data):
        for row in sheets_data:
            self.kiwi_parameters_no_stopover["fly_to"] = f"city:{row['iataCode']}"
            response = requests.get(
                url=self.FLIGHT_SEARCH_ENDPOINT,
                headers=self.kiwi_headers,
                params=self.kiwi_parameters_no_stopover
            ).json()
            if len(response["data"]) == 0:
                self.kiwi_parameters_one_stopover["fly_to"] = f"city:{row['iataCode']}"
                response = requests.get(
                    url=self.FLIGHT_SEARCH_ENDPOINT,
                    headers=self.kiwi_headers,
                    params=self.kiwi_parameters_one_stopover
                ).json()
            self.search_list.append(response)
            try:
                self.kiwi_parameters_no_stopover.pop("fly_to")
            except KeyError:
                self.kiwi_parameters_one_stopover.pop("fly_to")

