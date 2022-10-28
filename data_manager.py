import requests
import os


class DataManager:
    def __init__(self):
        self.city_dict = {}
        self.SHEETY_API_KEY = os.getenv("SHEETY_API_KEY")
        self.SHEETY_ENDPOINT = os.getenv("SHEETY_ENDPOINT")
        self.sheety_parameters_price = {
            "price": {}
        }
        self.headers = {
            "Authorization": self.SHEETY_API_KEY
        }

    def get_data_prices(self):
        return requests.get(url=f"{self.SHEETY_ENDPOINT}/prices", headers=self.headers).json()["prices"]

    def get_data_members(self):
        return requests.get(url=f"{self.SHEETY_ENDPOINT}/users", headers=self.headers).json()["users"]

    def city_names(self):
        data_sheet = self.get_data_prices()
        for row in range(len(data_sheet)):
            self.city_dict[row + 2] = data_sheet[row]["city"]

    def update_rows_with_city_codes(self, iata_city_codes):
        for row in self.city_dict:
            self.sheety_parameters_price["price"]["iataCode"] = iata_city_codes[row - 2]
            requests.put(url=f"{self.SHEETY_ENDPOINT}/prices/{row}", headers=self.headers, json=self.sheety_parameters_price)
            self.sheety_parameters_price["price"].pop("iataCode")





