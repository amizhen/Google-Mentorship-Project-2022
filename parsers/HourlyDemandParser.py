import requests
import json
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

#Test parser to get all the data for a certain year from new york, will generalize later for all the states
#Response should be a post request and years should be in string format
def getdemandict(state, year):
    region = regions[state]
    eia_key = open("key.txt", "r").read(40)
    url = "https://api.eia.gov/series/?api_key="+eia_key+"&series_id=EBA."+region+"-ALL.D.H"
    response = requests.request("POST", url)
    demand = {}
    if response.status_code == 200:
        data = json.loads(response.text)
        for thing in data["series"][0]["data"]:
            if thing[0][:4] == year:
                demand[thing[0]] = thing[1]
        return demand
    else:
        print("request ded")

if __name__ == "__main__":
    print(getdemandict("Arizona", "2022"))
