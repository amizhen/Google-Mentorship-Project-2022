from power_system import PowerSys
from parsers.SolarData import get_solar
from parsers.HourlyDemandParser import get_demand


def test(sys : PowerSys, loc : str) -> int:
    # Need dict for converting location to state or electrical grid region
    # solar_gen_data = get_solar(0, 0)[avg_whatever][monthly] # Need to decide between dni and ghi
    # usage_data = get_demand(loc, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022)