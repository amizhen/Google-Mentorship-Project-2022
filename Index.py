from datetime import datetime
from flask import Flask, jsonify, request, render_template

from power_system import PowerSys
from data import Data

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("Index.html", regions = list(Data.regions.keys()), regionsLen = len(Data.regions))

@app.route("/run", methods=["POST"])
def run():
    data = request.get_json()
    power_sys = PowerSys(data["region"], data["storageCap"], datetime(2020, 1, 1), datetime(2021, 1, 1), percentSatisfied=data["percentagePower"] / 100)
    
    for wind in data["windPlants"]:
        power_sys.add_wind((wind[0], wind[1]), data["windFarmSize"]) # 75-159 per farm

    for solar in data["solarPlants"]:
        power_sys.add_solar((solar[0], solar[1]), data["solarFarmSize"] * 1000 * 1000) # the amt here is the square km of solar panels. Can range f
    power_sys.run()

    return jsonify({
        "demand": {key.timestamp() : power_sys.demand[key] for key in power_sys.demand},
        "net_history": {key.timestamp() : power_sys.net_history[key] for key in power_sys.net_history},
        "storage_history": {key.timestamp() : power_sys.storage_history[key] for key in power_sys.storage_history},
        "gen_history": {key.timestamp() : power_sys.gen_history[key] for key in power_sys.gen_history},
        "waste_history": {key.timestamp() : power_sys.waste_history[key] for key in power_sys.waste_history}
    });

if __name__ == "__main__":
    app.run(debug = True)    
