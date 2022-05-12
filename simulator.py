from data.Data import get_solar_data, get_wind_data, get_electric_demand
from power_system import PowerSys
from datetime import datetime

def run(sys : PowerSys, loc : str, start : datetime, end : datetime) -> None:
    """
    :param sys: Takes a power setup
    :param loc: Takes a location
    :param start: Start Date (find min/max)
    :param end: End Date (find min/max)
    :return: modifies the fitness parameter of the input power system (maybe returns other useful info about run)
    """

    # Need to convert location to lat and longitute cords, maybe region too.

    lat = 42.355978782625336
    lon = -74.9824086324889

    wind_data = get_wind_data(lat, lon, start, end)
    solar_data = get_solar_data(lat, lon, start, end)
    demand = get_electric_demand(loc, start, end)


