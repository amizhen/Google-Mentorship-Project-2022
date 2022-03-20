import requests

eia_key = ' '
usage_url = f"https://api.eia.gov/series/?api_key={eia_key}&series_id=EBA.NY-ALL.D.H"

response_usage = requests.request("POST", usage_url)

if __name__ == "__main__":
    if response_usage.status_code == 200:
        print(response_usage.text)







