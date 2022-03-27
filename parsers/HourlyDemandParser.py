from typing import Mapping
import requests

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

def getdemandict(state : str, year : int) -> Mapping[str, int]:
    eia_key = open("key.txt", "r").read(40)
    response = requests.get(f"https://api.eia.gov/series/?api_key={eia_key}&series_id=EBA.{regions[state]}-ALL.D.H")
    if response.status_code == 200:
        data = response.json()
        return {datum[0] : datum[1] for datum in data["series"][0]["data"] if datum[0][:4] == str(year)}
    else:
        print("Request Failed")

if __name__ == "__main__":
    print(getdemandict("Arizona", 2015))
