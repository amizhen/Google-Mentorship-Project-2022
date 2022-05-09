import math


def wind_height(speed_10 : float, speed_50 : float, roughness : float, target = 80.0):
    '''
    :param speed_10: Wind speed at 10 meters
    :param speed_50: Wind speed at 50 meters
    :param roughness: Surface roughness
    :param target: Optional target height, defaults to 80 meters.
    :return: the speed at target height
    '''
    return speed_10 * math.log(target/roughness) / math.log(10/roughness)


def find_roughness(speeds_10 : dict, speeds_50 : dict):
    '''
    :param speeds_10: however much of hourly speed data at 10 meters
    :param speeds_50: however much of hourly speed data at 50 meters.
    It is assumed that both data sets start at the same date.
    :return: The average calculated rougness
    '''
    total = min(len(speeds_10), len(speeds_50))
    speeds_10 = speeds_10.values()
    speeds_50 = speeds_50.values()
    for i in range(total):
        speeds_10[i]


def rougness_formula(speed_10 : float, speed_50 : float):
    



def get_wind_power(air_density : float, radius : float, wind_velocity : float, efficiency : float) -> float:
    """
    Function to calculate the power (joules per second) produced by a wind turbine

    Formula retrieved from https://www.raeng.org.uk/publications/other/23-wind-turbine 

    Args:
        air_density : The density of the air in kg/m^3
        radius : The length of the wind turbine in m
        wind_velocity : The velocity of the wind in m/s
        efficiency : 
            The efficency of the wind turbines. The theoretical max is 16/27 according to Betz's limit

    Returns:
        The power (J/s) (Watts) produced by the wind turbine
    """

    return 0.5 * air_density * radius ** 2 * math.pi * wind_velocity ** 3 * efficiency

def get_solar_power(irradiance : float, panel_area : float, efficiency : float = 0.15) -> float:
    """
    Function to calculate the power (joules per second) produced by solar panels

    Args:
        irradiance : The irradiance (W/m^2)
        length : length of solar panel
        width : width of solar panel
        efficiency : efficiency of solar panel. Range is usually between 15% to 18%

    Returns:
        The power (J/s) produced by the solar panel
    """

    return irradiance * panel_area * efficiency

if __name__ == "__main__":
    # print(get_solar_power(200, 10, 10))
    # print(get_wind_power(1.23, 52, 13.37, 0.4))
    # print(wind_height(5.0, 100.0, 0.03))
