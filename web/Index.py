from flask import Flask, request, render_template

app = Flask(__name__)
b = {"lng": 1, "lat": 1}

with open("web\\mapkey.txt", "r") as file:
    mapbox_access_token = file.read(90)

@app.route("/")
def index():
    return render_template('Index.html',
        mapbox_access_token=mapbox_access_token)

@app.route("/dataget", methods=["POST"])
def coords_to_locale():
    data = request.get_json()
    b["lng"] = data["lng"]
    b["lat"] = data["lat"]
    return f"({b['lat']}, {b['lng']})"

if __name__ == "__main__":
    app.run(debug = True)    
