import requests
import json

url = "http://api.eia.gov/series/?api_key=YOUR_API_KEY_HERE&series_id=EBA.NY-ALL.D.H"

test = requests.request("POST", url)

#Test parser to get all the data for a certain year from new york, will generalize later for all the states
def getdemandict(response, year):
    demand = {}
    data = json.loads(response.text)
    for thing in data["series"][0]["data"]:
        if thing[0][:4] == year:
            demand[thing[0]] = thing[1]
    return demand

if __name__ == "__main__":
    print(getdemandict(test, "2022"))
