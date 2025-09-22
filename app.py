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
    chart_args = {
        "name": data.get("name", ""),
        "year": int(data.get("year", 1983)),
        "month": int(data.get("month", 11)),
        "day": int(data.get("day", 4)),
        "hour": int(data.get("hour", 19)),
        "minute": int(data.get("minute", 20)),
        "nation": data.get("nation", "BR"),
        "city": data.get("city", "Rio de Janeiro"),
        "lat": float(data.get("lat", -22.92409)),
        "lng": float(data.get("lng", -43.21102)),
        "tz_str": data.get("tz_str", "America/Sao_Paulo")
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
    try:
        AstrologyChartView(**chart_args)
    except Exception as e:
        print(f"Application error: {e}")

if __name__ == "__main__":
    port = 5000
    url = f"http://127.0.0.1:{port}/"
    webbrowser.open(url)
    app.run(port=port, debug=True, use_reloader=False)