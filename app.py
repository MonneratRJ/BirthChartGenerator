# app.py
from views.astrology_chart_view import AstrologyChartView
from flask import Flask, send_from_directory, jsonify, request
import webbrowser
from entities.astrology_chart import AstrologyChartEntity

app = Flask(__name__, static_folder="static")

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

@app.route("/api/chart", methods=["POST"])
def chart_data():
    data = request.get_json()
    required_fields = ["name", "year", "month", "day", "hour", "minute", "country", "city", "lat", "lng", "tz_str"]
    missing = [f for f in required_fields if f not in data or data[f] in (None, "")]
    if missing:
        print(f"[ERROR] Missing required fields: {missing}")
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400
    chart_args = {
        "name": data["name"],
        "year": int(data["year"]),
        "month": int(data["month"]),
        "day": int(data["day"]),
        "hour": int(data["hour"]),
        "minute": int(data["minute"]),
        "country": data["country"],
        "city": data["city"],
        "lat": float(data["lat"]),
        "lng": float(data["lng"]),
        "tz_str": data["tz_str"]
    }
    chart = AstrologyChartEntity(**chart_args)
    planets = []
    for planet in chart.get_planetary_positions() or []:
        planets.append({
            "name": getattr(planet, "name", ""),
            "sign": getattr(planet, "sign", ""),
            "degree": getattr(planet, "abs_pos", ""),
            "house": getattr(planet, "house", "")
        })
    house_labels = ["Ascendant", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
    houses = []
    for i, house in enumerate(chart.get_house_cusps() or []):
        houses.append({
            "name": house_labels[i] if i < len(house_labels) else f"House {i+1}",
            "degree": getattr(house, "abs_pos", ""),
            "sign": getattr(house, "sign", "")
        })
    return jsonify({"planets": planets, "houses": houses})

def main():
    print("BirthChartGenerator app started.")

if __name__ == "__main__":
    port = 5000
    url = f"http://127.0.0.1:{port}/"
    webbrowser.open(url)
    app.run(port=port, debug=True, use_reloader=False)