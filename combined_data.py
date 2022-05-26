from datetime import datetime
from util.Formula import find_roughness, calc_higher_speed, calc_wind_power, convert_to_ghi_data, calc_solar_power
from data.Data import get_wind_data_10m, get_wind_data_50m, get_solar_data

def get_wind(start, end, lon, lat, radius, height):
    wind_data10m = get_wind_data_10m(lon, lat, start, end)
    wind_data50m = get_wind_data_50m(lon, lat, start, end)
    roughness = find_roughness(wind_data10m,wind_data50m)
    wind_data80m = {time : calc_higher_speed(wind_data50m[time], roughness, height) for time in wind_data50m}
    wind_power = {time : calc_wind_power(radius, wind_data80m[time]) for time in wind_data80m}
    return wind_power

def get_solar(start, end, lon, lat, efficiency):
    solar_data = get_solar_data(lon, lat, start, end)
    ghi = convert_to_ghi_data(solar_data)
    solar_power = {time : calc_solar_power(ghi[time], efficiency) for time in ghi}
    return solar_power




