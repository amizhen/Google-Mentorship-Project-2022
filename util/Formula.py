
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


if __name__ == "__main__":
    print(get_wind_power(1.23, 52, 12, 0.4))