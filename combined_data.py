from datetime import datetime
from util.Formula import find_roughness, calc_higher_speed, calc_wind_power
from data.Data import get_wind_data_10m, get_wind_data_50m

def get_wind(start, end, lon, lat, radius, height = 80):
    windData10m = get_wind_data_10m(lon, lat, start, end)
    windData50m = get_wind_data_50m(lon, lat, start, end)
    roughness = find_roughness(windData10m,windData50m)
    windData80m = {time : calc_higher_speed(windData50m[time], roughness, target=height) for time in windData50m}
    windPower = {time : calc_wind_power(radius, windData80m[time]) for time in windData80m}
    return windPower

# def get_solar(start, end, lon, lat):
