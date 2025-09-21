# app.py
from views.astrology_chart_view import AstrologyChartView
from flask import Flask, send_from_directory, jsonify
import webbrowser
from entities.astrology_chart import AstrologyChartEntity
import os

app = Flask(__name__, static_folder="static")

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

@app.route("/api/chart")
def chart_data():
    chart_args = {
        "name": "Marcelo Monnerat Castello",
        "year": 1983,
        "month": 11,
        "day": 4,
        "hour": 19,
        "minute": 20,
        "nation": "BR",
        "city": "Rio de Janeiro",
        "lat": -22.92409,
        "lng": -43.21102,
        "tz_str": "America/Sao_Paulo"
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
    houses = []
    for i, house in enumerate(chart.get_house_cusps() or []):
        houses.append({
            "name": f"House {i+1}",
            "degree": getattr(house, "abs_pos", "")
        })
    return jsonify({"planets": planets, "houses": houses})

def main():
    chart_args = {
        "name": "Marcelo Monnerat Castello",
        "year": 1983,
        "month": 11,
        "day": 4,
        "hour": 19,
        "minute": 20,
        "city": "Rio de Janeiro",
        "nation": "BR",
        "lat": -22.92409,
        "lng": -43.21102,
        "tz_str": "America/Sao_Paulo"
    }
    try:
        AstrologyChartView(**chart_args)
    except Exception as e:
        print(f"Application error: {e}")

if __name__ == "__main__":
    port = 5000
    url = f"http://127.0.0.1:{port}/"
    webbrowser.open(url)
    app.run(port=port, debug=True)