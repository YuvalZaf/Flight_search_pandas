import requests
import datetime
import pandas as pd



URL = "https://tequila-api.kiwi.com/locations/query"
TEQUILA_SEARCH_URL = "https://api.tequila.kiwi.com/v2/search"
API_KEY = "YOUR KEY HERE"


class FlightSearch:
    def __init__(self):  # constructor + incase you want to search fo flight from tomorrow till six months from now
        self.today =datetime.datetime.now().strftime("%d/%m/%Y")  # today date ant time
        self.six_months = (datetime.datetime.now() + datetime.timedelta(days=6 * 30)).strftime(
            "%d/%m/%Y")  # search for flights in six months period

    def get_country(self, destinations, manager): # search for city/airport code in kiwi web.
        headers = {"apikey": API_KEY}
        data = manager.create_data()
        for _, i in destinations[["City", "iata code"]].iterrows():
            name = i["iata code"]
            if pd.isna(name):
                query = {"term": i["City"], "location_types": "city"}
                response = requests.get(url=URL, headers=headers, params=query)
                updated = response.json()  # change the data to json format to read it
                final = updated["locations"][0]["code"]  # need to take specific field from the response(only IATA)
                row_index = data.loc[data["City"] == i["City"]].index[0]
                data.at[row_index,"iata code"] = final
                manager.update_data()

    def search_for_flights(self, origin, manager):   # search for the cheapest flight for your destinations
        headers = {"apikey": API_KEY}
        full_data = manager.create_data()
        for i in full_data.iterrows():
            query = {  # the data i want to receive from the API
                "fly_from": origin,
                "fly_to": i[1]["iata code"],
                "date_from": i[1]["From date"].date().strftime("%d/%m/%Y"),
                "date_to": i[1]["To date"].date().strftime("%d/%m/%Y"),
                "nights_in_dst_from": i[1]["LB nights"],
                "nights_in_dst_to": i[1]["UB nights"],
                "one_for_city": 1,
                "flight_type": "round",
                "max_stopovers": 0,
                "curr": "ILS"
            }
            response = requests.get(url=TEQUILA_SEARCH_URL, headers=headers, params=query)
            response.raise_for_status()
            try:  # update the data from the API to your excel sheet
                row_index = full_data.loc[full_data["City"] == i[1]["City"]].index[0]
                data = response.json()["data"][0]
                full_data.loc[row_index, 'Landing'] = data["flyTo"]
                full_data.loc[row_index, 'Price'] = data["price"]
                full_data.loc[row_index, 'Date Flight'] = data["local_departure"].split("T")[0]
                full_data.loc[row_index, 'Flight num'] = data["route"][0]["flight_no"]
                full_data.loc[row_index, 'Date return'] = data["route"][1]["local_departure"].split("T")[0]
                full_data.loc[row_index, 'Link'] = data["deep_link"]
                manager.update_data()

            except IndexError:
                print(f"No flights found for city.")







