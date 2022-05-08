import math


def change_wind_altitude(speed_10 : float, speed_50 : float, target = 80.0):
    '''
    :param speed_10: Wind speed at 10 meters
    :param speed_50: Wind speed at 50 meters
    :param target: Optional target height, defaults to 80 meters.
    :return:
    '''

    roughness = [0.0002, 0.0024, 0.03, ]



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
    print(get_solar_power(200, 10, 10))
    print(get_wind_power(1.23, 52, 13.37, 0.4))