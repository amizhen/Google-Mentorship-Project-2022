from datetime import date
import pprint
from data.Data import TimeRange, get_electric_demand, get_solar_data, get_wind_data

if __name__ == "__main__":
    pprint.pprint(get_solar_data(42.355978782625336, -74.9824086324889, date(2020, 1, 1), date(2020, 1, 2)))
    # pprint.pprint(get_wind_data(42.355978782625336, -74.9824086324889, TimeRange.EVERY_WEEK))
    # pprint.pprint(get_electric_demand("Arizona", 2015))

    # t = get_wind_data(42.355978782625336, -74.9824086324889, TimeRange.EVERY_TWO_WEEK)