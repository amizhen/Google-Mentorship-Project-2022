from datetime import datetime
import pprint
from data.Data import get_electric_demand_in_range, get_solar_data, get_wind_data, get_wind_data_in_range

if __name__ == "__main__":
    pprint.pprint(get_solar_data(42.355978782625336, -74.9824086324889, datetime(2007, 3, 1), datetime(2007, 3, 2)))

    pprint.pprint(get_wind_data_in_range(42.355978782625336, -74.9824086324889, datetime(2007, 3, 1), datetime(2007, 3, 2)))

    pprint.pprint(get_electric_demand_in_range("New York", datetime(2007, 3, 1), datetime(2007, 3, 2)))