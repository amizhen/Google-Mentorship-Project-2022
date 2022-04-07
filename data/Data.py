from enum import IntEnum
from typing import Mapping, Union

import requests
import h5pyd
import pandas as pd

from util.WTKUtil import WTK_idx

regions = {
    "California" : "CAL", 
    **dict.fromkeys(["North Carolina", "South Carolina"], "CAR"),
    **dict.fromkeys(["North Dakota", "South Dakota", "Nebraska", "Kansas", "Oklahoma", "Minnesota"],"CENT"),
    "Florida" : "FLA",
    **dict.fromkeys(["Delaware", "Maryland", "New Jersey", "Pennsylvania", "Virginia", "West Virginia", "District of Columbia"], "MIDA"),
    **dict.fromkeys(["Illinois", "Indiana", "Iowa", "Michigan", "Ohio", "Wisconsin", "Missouri"], "MIDW"),
    **dict.fromkeys(["Connecticut", "Maine", "Massachusetts", "New Hampshire", "Rhode Island", "Vermont"], "NE"),
    "New York" : "NY",
    **dict.fromkeys(["Oregon", "Washington", "Idaho", "Montana", "Wyoming"], "NW"),
    **dict.fromkeys(["Alabama", "Georgia", "Arkansas", "Kentucky", "Louisiana", "Mississippi"], "SE"),
    **dict.fromkeys(["Arizona", "New Mexico", "Utah", "Nevada", "Colorado"], "SW"),
    "Tennessee" : "TEN",
    "Texas" : "TEX"  
}

class TimeRange(IntEnum):
    """
    A enum holding common periods in hours
    """

    EVERY_12_HOUR = 12
    EVERY_24_HOUR = 24
    EVERY_WEEK = 24 * 7
    EVERY_TWO_WEEK = 24 * 14
    DAILY = EVERY_24_HOUR
    WEEKLY = EVERY_WEEK

with open("key.txt", "r") as file:
    API_KEY = file.read(40)

# So it only opens onces
WTK = h5pyd.File("/nrel/wtk-us.h5", "r", endpoint="https://developer.nrel.gov/api/hsds", api_key = API_KEY)

def get_solar_data(lat : float, lon : float) -> Mapping[str, Mapping[str, Union[float, Mapping[str, float]]]]:
    """
    A function that retrieves monthly solar data

    Args:
        lat : latitude
        lon : longitude

    Returns:
        A mapping of the solar data at the given position
    """
    response = requests.get(f'https://developer.nrel.gov/api/solar/solar_resource/v1.json?api_key={API_KEY}&lat={lat}&lon={lon}')
    if response.status_code == 200:
        return response.json()["outputs"]
    else:
        raise ValueError(f'Request Failed {response.status_code}')

def get_electric_demand(state : str, *years : int) -> Mapping[str, int]:
    """
    A function that retrieves electric demands of states. 

    Args:
        state : The state to retrieve data
        years : The years of the data to be retrieved

    Returns:
        A mapping of the datetime to the energy consumption
    """

    response = requests.get(f"https://api.eia.gov/series/?api_key={API_KEY}&series_id=EBA.{regions[state]}-ALL.D.H")
    if response.status_code == 200:
        data = response.json()
        return {datum[0] : datum[1] for datum in data["series"][0]["data"] if int(datum[0][:4]) in years}
    else:
        raise ValueError(f'Request Failed {response.status_code}')

def get_wind_data(lat : float, lon : float, skip : Union[TimeRange, int] = TimeRange.EVERY_WEEK) -> Mapping[pd.Timestamp, float]:
    """
    A function that retrieves wind data

    Args:
        lat : latitude
        lon : longitude
        skip : The period of time to skip between data points

    Returns:
        A mapping of timestamp to the wind speed data
    """

    wtk_ij = WTK_idx(WTK, (lat, lon))

    dt = pd.to_datetime(WTK['datetime'][:].astype(str))[12::skip]
    ds = WTK["windspeed_80m"][12::skip, wtk_ij[0], wtk_ij[1]]

    return {dt[i] : ds[i] for i in range(len(dt))}