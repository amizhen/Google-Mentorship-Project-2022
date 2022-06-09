from datetime import datetime
import pprint

import combined_data
from data.Data import get_electric_demand, get_solar_data, get_wind_data_10m, get_wind_data_50m
from util.Formula import find_roughness, convert_to_ghi_data, calc_solar_power
from util.Formula import roughness_formula, calc_higher_speed

if __name__ == "__main__":
    """ print('Solar')
    pprint.pprint(get_solar_data(42.355978782625336, -74.9824086324889, datetime(2007, 3, 1), datetime(2007, 3, 2)))
    print('Wind')
    pprint.pprint(get_wind_data(42.355978782625336, -74.9824086324889, datetime(2007, 3, 1), datetime(2007, 3, 2)))
    print('Demand')
    pprint.pprint(get_electric_demand("New York", datetime(2007, 3, 1), datetime(2007, 3, 4)))
    print("Wind Speed 10m")
    pprint.pprint(get_wind_data_10m(42.355978782625336, -74.9824086324889, datetime(2007, 3, 1), datetime(2007, 3, 2)))
    print("Wind Speed 50m")
    pprint.pprint(get_wind_data_50m(42.355978782625336, -74.9824086324889, datetime(2007, 3, 1), datetime(2007, 3, 2))) """

    # print('Solar')
    # solar_data = get_solar_data(42.355978782625336, -74.9824086324889, datetime(2007, 3, 1), datetime(2007, 3, 2))
    # # pprint.pprint(solar_data)
    # print()
    # ghi = convert_to_ghi_data(solar_data)
    # pprint.pprint(ghi)
    # print()
    # pprint.pprint({time: calc_solar_power(ghi[time], 0.15) for time in ghi})

    from combined_data import get_solar, get_wind
    # print(get_wind(datetime(2007, 3, 1), datetime(2007, 3, 2), 42.355978782625336, -74.9824086324889, 40, 80))
    # pprint.pprint(get_solar(datetime(2007, 3, 1), datetime(2007, 3, 2), 42.355978782625336, -74.9824086324889, 40))
    pprint.pprint(get_electric_demand("New York", datetime(2016, 3, 1), datetime(2016, 3, 4)))
    # pprint.pprint(get_wind(datetime(2007, 3, 1), datetime(2007, 3, 2), 42.355978782625336, -74.9824086324889, 40, 80))
    # pprint.pprint(get_solar(datetime(2007, 3, 1), datetime(2007, 3, 2), 42.355978782625336, -74.9824086324889, 0.15))

