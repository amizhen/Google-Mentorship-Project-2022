from datetime import datetime
import pprint
from data.Data import get_electric_demand, get_solar_data, get_wind_data, get_wind_data

if __name__ == "__main__":
    print('Solar')
    pprint.pprint(get_solar_data(42.355978782625336, -74.9824086324889, datetime(2007, 3, 1), datetime(2007, 3, 2)))
    print('Wind')
    pprint.pprint(get_wind_data(42.355978782625336, -74.9824086324889, datetime(2007, 3, 1), datetime(2007, 3, 2)))
    print('Demand')
    pprint.pprint(get_electric_demand("New York", datetime(2007, 3, 1), datetime(2007, 3, 4)))