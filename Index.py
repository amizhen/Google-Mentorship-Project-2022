from datetime import datetime
from flask import Flask, jsonify, request, render_template

from power_system import PowerSys
from data import Data

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("Index.html", regions = list(Data.regions.keys()), regionsLen = len(Data.regions))

@app.route("/run", methods=["POST"])
def send_data():
    data = request.get_json()
    power_sys = PowerSys(data["region"], -1, datetime(2016, 3, 1), datetime(2016, 3, 4))
    
    for wind in data["windPlants"]:
        power_sys.add_wind((wind[0], wind[1]), 150) # 75-159 per farm

    for solar in data["solarPlants"]:
        power_sys.add_solar((solar[0], solar[1]), 4000000) # the amt here is the square meters of solar panels. Can range from 10 to 50 acres 

    power_sys.run()

    return jsonify({
        "net_history": {key.timestamp() : power_sys.net_history[key] for key in power_sys.net_history},
        "storage_history": {key.timestamp() : power_sys.storage_history[key] for key in power_sys.storage_history},
        "gen_history": {key.timestamp() : power_sys.gen_history[key] for key in power_sys.gen_history},
        "waste_history": {key.timestamp() : power_sys.waste_history[key] for key in power_sys.waste_history}
    });

if __name__ == "__main__":
    app.run(debug = True)    
