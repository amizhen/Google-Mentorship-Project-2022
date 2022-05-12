from argparse import ArgumentError
from datetime import datetime, timedelta
import functools

import requests

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

@functools.lru_cache(maxsize=3)
def get_wind_data_10m(lat: float, lon: float, start: datetime, end: datetime):
    end = end - timedelta(days=1)
    response = requests.get(
        f"https://power.larc.nasa.gov/api/temporal/hourly/point?start={start.strftime('%Y%m%d')}&end={end.strftime('%Y%m%d')}&latitude={lat}&longitude={lon}&community=re&parameters=WS10M&format=json&header=false&time-standard=utc")
    if response.status_code == 200:
        data = response.json()["properties"]["parameter"]["WS10M"]
        return {datetime.strptime(datum, "%Y%m%d%H"): data[datum] for datum in data}
    else:
        raise ValueError()

@functools.lru_cache(maxsize=3)
def get_wind_data_50m(lat: float, lon: float, start: datetime, end: datetime):
    end = end - timedelta(days=1)
    response = requests.get(
        f"https://power.larc.nasa.gov/api/temporal/hourly/point?start={start.strftime('%Y%m%d')}&end={end.strftime('%Y%m%d')}&latitude={lat}&longitude={lon}&community=re&parameters=WS50M&format=json&header=false&time-standard=utc")
    if response.status_code == 200:
        data = response.json()["properties"]["parameter"]["WS50M"]
        return {datetime.strptime(datum, "%Y%m%d%H"): data[datum] for datum in data}
    else:
        raise ValueError()

@functools.lru_cache(maxsize=3)
def _get_electric_data(state : str):
    return requests.get(f"https://api.eia.gov/series/?api_key={API_KEY}&series_id=EBA.{regions[state]}-ALL.D.H")

@functools.lru_cache(maxsize=3)
def get_electric_demand(state: str, start: datetime, end: datetime):
    """
    A function that retrieves electric demands of states. 

    Args:
        state : The state to retrieve data
        start : the start datetime inclusive
        end : the end datetime exclusive

    Returns:
        A mapping of the datetime to the energy consumption in megawatthours
    """

    if end < start:
        raise ArgumentError(message="end_year must be greater or equal to than start_year")

    response = _get_electric_data(state)
    if (response.status_code == 200):
        data = response.json()

        return {datetime.strptime(datum[0], "%Y%m%dT%HZ"): datum[1] for datum in data["series"][0]["data"] if
                start <= datetime.strptime(datum[0], "%Y%m%dT%HZ") < end}
    else:
        raise ValueError(f"Request Failed {response.status_code}")

@functools.lru_cache(maxsize=3)
def get_solar_data(lat : float, lon : float, start : datetime, end : datetime):
    end -= timedelta(days=1) # api end is inclusive
    response = requests.get(
        f"https://power.larc.nasa.gov/api/temporal/hourly/point?start={start.strftime('%Y%m%d')}&end={end.strftime('%Y%m%d')}&latitude={lat}&longitude={lon}&community=sb&parameters=SZA%2CCLRSKY_SFC_SW_DNI%2CCLRSKY_SFC_SW_DIFF&format=json&header=false&time-standard=utc"
    )

    if response.status_code == 200:
        json = response.json()["properties"]["parameter"]
        data = {}
        for parameter in json:
            data[parameter] = {}
            data[parameter] = {datetime.strptime(datum, "%Y%m%d%H") : max(json[parameter][datum], 0) for datum in json[parameter]}
        return data
    return