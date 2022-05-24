from datetime import datetime
import pprint
from data.Data import get_electric_demand, get_solar_data, get_wind_data_10m, get_wind_data_50m
from util.Formula import find_roughness, convert_to_ghi_data
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
    #
    print('Solar')
    solar_data = get_solar_data(42.355978782625336, -74.9824086324889, datetime(2007, 3, 1), datetime(2007, 3, 2))
    # pprint.pprint(solar_data)
    print()
    ghi = convert_to_ghi_data(solar_data)
    pprint.pprint(ghi)

    # from combined_data import get_wind, calc_wind_power
    # print(get_wind(datetime(2007, 3, 1), datetime(2007, 3, 2), 42.355978782625336, -74.9824086324889, 40))
