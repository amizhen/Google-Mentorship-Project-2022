from datetime import datetime
import math
from typing import Mapping


def calc_higher_speed(speed_50: float, roughness: float, target):
    '''
    :param speed_50: Wind speed at 50 meters
    :param roughness: Surface roughness
    :param target: Optional target height, defaults to 80 meters.
    :return: the speed at target height
    See for more details and formula:
    https://wind-data.ch/tools/profile.php?h=10&v=5&z0=0.03&abfrage=To+update
    '''
    return speed_50 * math.log(target / roughness) / math.log(50 / roughness)


def find_roughness(speeds_10: dict, speeds_50: dict):
    '''
    :param speeds_10: however much of hourly speed data at 10 meters
    :param speeds_50: however much of hourly speed data at 50 meters.
    It is assumed that both data sets start at the same date.
    :return: The average calculated roughness
    See for more details and formula:
    https://wind-data.ch/tools/profile.php?h=10&v=5&z0=0.03&abfrage=To+update
    '''
    total = min(len(speeds_10), len(speeds_50))
    speeds_10 = list(speeds_10.values())
    speeds_50 = list(speeds_50.values())
    sum = 0
    for i in range(total):
        sum += roughness_formula(speeds_10[i], speeds_50[i])
    return sum / total


def roughness_formula(speed_10: float, speed_50: float):
    '''
    :param speed_10: Speed at 10 meters
    :param speed_50: Speed at 50 meters
    :return: Roughness
    Helper fuction for finding the roughness given wind speed at 50 and 10 meters
    '''
    return (10 ** speed_50 / 50 ** speed_10) ** (1.0 / (speed_50 - speed_10))


def calc_wind_power(radius: float, wind_velocity: float, efficiency=0.4, air_density=1.2041) -> float:
    """
    Function to calculate the power (joules per second) produced by a wind turbine

    Formula retrieved from https://www.raeng.org.uk/publications/other/23-wind-turbine 

    Args:
        air_density : The density of the air in kg/m^3
        radius : The length of the wind turbine in m
        wind_velocity : The velocity of the wind in m/s
        efficiency : 
            The efficency of the wind turbines. The theoretical max is 16/27 according to Betz's limit,
            however in practice it is between 35-45.

    Returns:
        The power (Megawatt hours) produced by the wind turbine, with an aditional coefficant of 0.6 to account for
        mechanical losses.
    """

    return 0.5 * air_density * (radius ** 2) * math.pi * wind_velocity ** 3 * efficiency * 0.6 * (1 / (10 ** 6))


def calc_solar_power(GHI: float, efficiency: float) -> float:
    """
    Function to calculate the power (joules per second) produced by solar panels per square meter

    Args:
        irradiance : The irradiance (W/m^2)
        length : length of solar panel
        width : width of solar panel
        efficiency : efficiency of solar panel. Range is usually between 15% to 18%

    Returns:
        The power (megawatt hours) produced by the solar panel
    """
    # The 0.75 is to account for dirt, shade, etc
    return GHI * efficiency * 0.75 * (1 / (10 ** 6))


def get_ghi(zenith: float, dni: float, dhi: float):
    return math.cos(math.radians(zenith)) * dni + dhi


def convert_to_ghi_data(data: Mapping[str, Mapping[datetime, float]]) -> Mapping[datetime, float]:
    # try:
    converted = {}
    for key in data["SZA"]:
        converted.update(
            {key: get_ghi(data["SZA"][key], data["CLRSKY_SFC_SW_DNI"][key], data["CLRSKY_SFC_SW_DIFF"][key])})

    return converted
    # except:
    #     raise ValueError("Incorrectly formatted Mapping - Should be from get_solar_data func")


if __name__ == "__main__":
    # print(get_solar_power(200, 10, 10))
    # print(get_wind_power(1.23, 52, 13.37, 0.4))
    # print(wind_height(5.0, 100.0, 0.03))
    # The keys don't matter for these test cases
    print(find_roughness({1.0: 5.0}, {1.0: 6.39}))  # should be 0.03
    print(find_roughness({1.0: 5.7}, {1.0: 6.55}))  # should be 0.0002
    print(find_roughness({1.0: 5.7, 2.0: 3.0, 3.0: 10},
                         {1.0: 6.55, 2.0: 3.45, 3: 11.49, 10000: 10000}))  # should be 0.0002
