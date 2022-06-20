from datetime import datetime
from flask import Flask, jsonify, request, render_template

from power_system import PowerSys
from data import Data

app = Flask(__name__)


region = list(Data.regions.keys())[0];

power_sys = PowerSys(region, -1, datetime(2016, 3, 1), datetime(2016, 3, 4))

@app.route("/")
def index():
    return render_template("Index.html", regions = list(Data.regions.keys()), regionsLen = len(Data.regions))

@app.route("/place/wind", methods=["POST"])
def place_wind():
    data = request.get_json()
    power_sys.add_wind((data["lat"], data["lng"]), 150) # 75-150 per farm
    return jsonify({})

@app.route("/place/solar", methods=["POST"])
def place_solar():
    data = request.get_json()
    power_sys.add_solar((data["lat"], data["lng"]), 4000000) # the amt here is the square meters of solar panels. Can range from 10 to 50 acres 
    return jsonify({})

@app.route("/changeRegion", methods=["POST"])
def change_region():
    data = request.get_json()
    power_sys.set_region(data["region"])
    print("Registered")
    print(power_sys.region)
    return jsonify({})

@app.route("/remove/wind", methods=["POST"])
def remove_wind():
    return jsonify({});

@app.route("/run", methods=["POST"])
def send_data():
    power_sys.run();
    return jsonify({
        "net_history": {key.timestamp() : power_sys.net_history[key] for key in power_sys.net_history},
        "storage_history": {key.timestamp() : power_sys.storage_history[key] for key in power_sys.storage_history},
        "gen_history": {key.timestamp() : power_sys.gen_history[key] for key in power_sys.gen_history},
        "waste_history": {key.timestamp() : power_sys.waste_history[key] for key in power_sys.waste_history}
    });

if __name__ == "__main__":
    app.run(debug = True)    
