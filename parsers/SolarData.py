import requests
from typing import Mapping


def get_solar(lat : float, lon : float) -> Mapping[str, dict]:
    with open("key.txt", "r") as file:
        eia_key = file.readline()
    url = f'https://developer.nrel.gov/api/solar/solar_resource/v1.json?api_key={eia_key}&lat={lat}&lon={lon}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['outputs']
        # return {datum[0] : datum[1] for datum in data["series"][0]["data"] if datum[0][:4] == str(year)}
    else:
        raise ValueError(f'Request Failed {response.status_code}')

if __name__ == '__main__':
    print(get_solar(42.355978782625336, -74.9824086324889))