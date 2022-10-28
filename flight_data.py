import requests
from data_manager import DataManager
import os


class FlightData:
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
        self.iata_list = []
        self.flight_deal_details = []
        self.KIWI_API_KEY = os.environ.get("KIWI_API_KEY")
        self.KIWI_LOCATION_SEARCH = "https://tequila-api.kiwi.com/locations"
        self.kiwi_parameters = {
            "location_types": "city",
        }
        self.kiwi_headers = {
            "apikey": self.KIWI_API_KEY,
        }
        # self.city_diction = {2: 'Paris', 3: 'Berlin', 4: 'Tokyo', 5: 'Sydney', 6: 'Istanbul', 7: 'Kuala Lumpur', 8: 'New York', 9: 'San Francisco', 10: 'Cape Town'}

    def location_iata_response(self):
        for row in self.data_manager.city_dict:
            self.kiwi_parameters["term"] = self.data_manager.city_dict[row]
            response = requests.get(
                url=f"{self.KIWI_LOCATION_SEARCH}/query",
                params=self.kiwi_parameters,
                headers=self.kiwi_headers
            ).json()["locations"][0]["code"]
            self.iata_list.append(response)
            self.kiwi_parameters.pop("term")

    def cheapest_flight_details(self, flight_results, sheets_data):
        for option in flight_results:
            if len(option["data"]) != 0:
                for row in sheets_data:
                    if row["iataCode"] == option["data"][0]["cityCodeTo"]:
                        if option["data"][0]["price"] < row["lowestPrice"]:
                            if len(option["data"][0]["route"]) == 2:
                                self.flight_deal_details.append(
                                    {
                                        "price": option["data"][0]["price"],
                                        "fly_from": f"{option['data'][0]['cityFrom']}-{option['data'][0]['flyFrom']}",
                                        "fly_to": f"{option['data'][0]['cityTo']}-{option['data'][0]['flyTo']}",
                                        "date_from": f"{option['data'][0]['route'][0]['local_departure'][:10]}",
                                        "date_to": f"{option['data'][0]['route'][1]['local_departure'][:10]}",
                                    }
                                )
                            else:
                                self.flight_deal_details.append(
                                    {
                                        "price": option["data"][0]["price"],
                                        "fly_from": f"{option['data'][0]['cityFrom']}-{option['data'][0]['flyFrom']}",
                                        "fly_to": f"{option['data'][0]['cityTo']}-{option['data'][0]['flyTo']}",
                                        "date_from": f"{option['data'][0]['route'][0]['local_departure'][:10]}",
                                        "date_to": f"{option['data'][0]['route'][-1]['local_departure'][:10]}",
                                        "stop_over": f"{option['data'][0]['route'][0]['cityTo']}"
                                    }
                                )



