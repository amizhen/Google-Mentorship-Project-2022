
import math

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
        The power (J/s) produced by the wind turbine
    """

    return 0.5 * air_density * radius ** 2 * math.pi * wind_velocity ** 3 * efficiency

def get_solar_power(irradiance : float, length : float, width : float, efficiency : float = 0.15) -> float:
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

    return irradiance * length * width * efficiency

if __name__ == "__main__":
    print(get_solar_power(200, 10, 10))
    print(get_wind_power(1.23, 52, 13.37, 0.4))