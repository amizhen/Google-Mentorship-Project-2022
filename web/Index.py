from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# b = {"lng": 1, "lat": 1}

@app.route("/")
def index():
    return render_template("Web.html")

@app.route("/place/wind", methods=["POST"])
def place_wind():
    data = request.get_json()
    return jsonify({"lng": data["lng"], "lat": data["lat"]}) # placeholder

@app.route("/place/solar", methods=["POST"])
def place_solar():
    data = request.get_json()
    return jsonify({"lng": data["lng"], "lat": data["lat"]})

@app.route("/remove/wind", methods=["POST"])
def remove_wind():
    return jsonify({});

@app.route("/api/data")
def send_data():
    return jsonify({});

if __name__ == "__main__":
    app.run(debug = True)    
