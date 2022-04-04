import requests

with open("key.txt", "r") as file:
    eia_key = file.readline()
usage_url_eia = f"https://api.eia.gov/series/?api_key={eia_key}&series_id=EBA.NY-ALL.D.H"

lat = 42.355978782625336
lon = -74.9824086324889
usage_url_nrel = f'https://developer.nrel.gov/api/solar/solar_resource/v1.json?api_key={eia_key}&lat={lat}&lon={lon}'

response_usage = requests.get(usage_url_nrel)

if __name__ == "__main__":
    if response_usage.status_code == 200:
        print(response_usage.text)






