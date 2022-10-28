import data_manager
import flight_data
import flight_search
import notification_manager
import pprint

data_manager = data_manager.DataManager()

## Get city names from the Google Spreadsheet

# data_manager.city_names()
# city_dict = data_manager.city_dict

flight_data = flight_data.FlightData(data_manager)

## Update IATA codes for cities from spreadsheet, if not updated, with code commented out below

# flight_data.location_iata_response()
# list_of_city_codes = flight_data.iata_list
# data_manager.update_rows_with_city_codes(list_of_city_codes)

## Get full sheets data about service users and locations for the flight
sheets_data = data_manager.get_data_prices()
members_data = data_manager.get_data_members()

## Initiate a search for the cheapest flight, comparing to the historic minimum recorded in spreadsheets
flight_search = flight_search.FlightSearch()
flight_search.cheapest_flight_search(sheets_data)
flight_results = flight_search.search_list

## Show flight details and list of deals found, if any
flight_data.cheapest_flight_details(flight_results=flight_results, sheets_data=sheets_data)
list_of_deals = flight_data.flight_deal_details

## Send notifications to the users with details of deals found
notification_manager = notification_manager.NotificationManager()
messages = notification_manager.create_msg(list_of_deals)
list_of_msgs_to_send = notification_manager.list_of_messages
notification_manager.send_msg(members_data)
