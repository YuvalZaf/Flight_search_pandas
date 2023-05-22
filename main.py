from data import Data
from searchers import FlightSearch


ORIGIN = "TLV"

my_data = Data()
data = my_data.create_data()
my_searches = FlightSearch()
my_searches.search_for_flights(origin=ORIGIN, manager=my_data)



