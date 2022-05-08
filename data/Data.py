from argparse import ArgumentError
from datetime import datetime, timedelta
from typing import Mapping, Union

import requests
import h5pyd
import pandas as pd

from util.WTKUtil import WTK_idx

regions = {
    "California": "CAL",
    **dict.fromkeys(["North Carolina", "South Carolina"], "CAR"),
    **dict.fromkeys(["North Dakota", "South Dakota", "Nebraska", "Kansas", "Oklahoma", "Minnesota"], "CENT"),
    "Florida": "FLA",
    **dict.fromkeys(
        ["Delaware", "Maryland", "New Jersey", "Pennsylvania", "Virginia", "West Virginia", "District of Columbia"],
        "MIDA"),
    **dict.fromkeys(["Illinois", "Indiana", "Iowa", "Michigan", "Ohio", "Wisconsin", "Missouri"], "MIDW"),
    **dict.fromkeys(["Connecticut", "Maine", "Massachusetts", "New Hampshire", "Rhode Island", "Vermont"], "NE"),
    "New York": "NY",
    **dict.fromkeys(["Oregon", "Washington", "Idaho", "Montana", "Wyoming"], "NW"),
    **dict.fromkeys(["Alabama", "Georgia", "Arkansas", "Kentucky", "Louisiana", "Mississippi"], "SE"),
    **dict.fromkeys(["Arizona", "New Mexico", "Utah", "Nevada", "Colorado"], "SW"),
    "Tennessee": "TEN",
    "Texas": "TEX"
}

with open("key.txt", "r") as file:
    API_KEY = file.read(40)

# So it only opens onces
WTK = h5pyd.File("/nrel/wtk-us.h5", "r", endpoint="https://developer.nrel.gov/api/hsds", api_key=API_KEY)


def get_solar_data(lat: float, lon: float, start: datetime, end: datetime):
    end = end - timedelta(days=1);
    response = requests.get(
        f"https://power.larc.nasa.gov/api/temporal/hourly/point?start={start.strftime('%Y%m%d')}&end={end.strftime('%Y%m%d')}&latitude={lat}&longitude={lon}&community=re&parameters=ALLSKY_SFC_LW_DWN&format=json&header=false&time-standard=utc")
    if response.status_code == 200:
        data = response.json()["properties"]["parameter"]["ALLSKY_SFC_LW_DWN"]
        return {datetime.strptime(datum, "%Y%m%d%H"): data[datum] for datum in data}
    else:
        raise ValueError()

def get_wind_data_10m(lat: float, lon: float, start: datetime, end: datetime):
    end = end - timedelta(days=1);
    response = requests.get(
        f"https://power.larc.nasa.gov/api/temporal/hourly/point?start={start.strftime('%Y%m%d')}&end={end.strftime('%Y%m%d')}&latitude={lat}&longitude={lon}&community=re&parameters=WS10M&format=json&header=false&time-standard=utc")
    if response.status_code == 200:
        data = response.json()["properties"]["parameter"]["WS10M"]
        return {datetime.strptime(datum, "%Y%m%d%H"): data[datum] for datum in data}
    else:
        raise ValueError()

def get_wind_data_50m(lat: float, lon: float, start: datetime, end: datetime):
    end = end - timedelta(days=1);
    response = requests.get(
        f"https://power.larc.nasa.gov/api/temporal/hourly/point?start={start.strftime('%Y%m%d')}&end={end.strftime('%Y%m%d')}&latitude={lat}&longitude={lon}&community=re&parameters=WS50M&format=json&header=false&time-standard=utc")
    if response.status_code == 200:
        data = response.json()["properties"]["parameter"]["WS50M"]
        return {datetime.strptime(datum, "%Y%m%d%H"): data[datum] for datum in data}
    else:
        raise ValueError()


def get_electric_demand(state: str, start: datetime, end: datetime):
    """
    A function that retrieves electric demands of states. 

    Args:
        state : The state to retrieve data
        start : the start datetime inclusive
        end : the end datetime exclusive

    Returns:
        A mapping of the datetime to the energy consumption
    """

    if end < start:
        raise ArgumentError(message="end_year must be greater or equal to than start_year")

    response = requests.get(f"https://api.eia.gov/series/?api_key={API_KEY}&series_id=EBA.{regions[state]}-ALL.D.H")
    if (response.status_code == 200):
        data = response.json()
        return {datetime.strptime(datum[0], "%Y%m%dT%HZ"): datum[1] for datum in data["series"][0]["data"] if
                start <= datetime.strptime(datum[0], "%Y%m%dT%HZ") < end}
    else:
        raise ValueError(f"Request Failed {response.status_code}")


def get_wind_data(lat: float, lon: float, start: datetime, end: datetime):
    wtk_ij = WTK_idx(WTK, (lat, lon))

    epoch = datetime(2007, 1, 1)
    hr = timedelta(hours=1)
    print(int((start - epoch) / hr))
    ds = WTK["windspeed_80m"][int((start - epoch) / hr):int((end - epoch) / hr):1, wtk_ij[0], wtk_ij[1]]
    return {(start + hr * i): ds[i] for i in range(len(ds))}
