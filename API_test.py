from datetime import date, datetime
import pprint
from data.Data import TimeRange, get_electric_demand_in_range, get_solar_data, get_wind_data, get_wind_data_in_range

if __name__ == "__main__":
    pprint.pprint(get_solar_data(42.355978782625336, -74.9824086324889, datetime(2007, 3, 1), datetime(2007, 3, 2)))
    # pprint.pprint(get_wind_data(42.355978782625336, -74.9824086324889, TimeRange.EVERY_WEEK))


    # pprint.pprint(get_GHI(42.355978782625336, -74.9824086324889, 2019))
    # pprint.pprint(get_electric_demand("Arizona", 2015))

    # t = get_wind_data(42.355978782625336, -74.9824086324889, TimeRange.EVERY_TWO_WEEK)

    pprint.pprint(get_wind_data_in_range(42.355978782625336, -74.9824086324889, datetime(2007, 3, 1), datetime(2007, 3, 2)))

    pprint.pprint(get_electric_demand_in_range("New York", datetime(2007, 3, 1), datetime(2007, 3, 2)))