# entities/astrology_chart.py
import kerykeion as ke
import os
from dotenv import load_dotenv

load_dotenv()

class AstrologyChartEntity:
    def __init__(self, name, year, month, day, hour, minute, country, city, lat, lng, tz_str="America/Sao_Paulo"):
        self.name = name
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.city = city
        self.country = country
        self.lat = lat
        self.lng = lng
        self.tz_str=tz_str
        self.chart = None
        self.error = None
        self._create_chart()

    def _create_chart(self):
        try:
            geonames_username = os.getenv("GEONAMES_USERNAME", "")
            self.chart = ke.AstrologicalSubject(
                name=self.name,
                year=self.year,
                month=self.month,
                day=self.day,
                hour=self.hour,
                minute=self.minute,
                city=self.city,
                nation=self.country,
                lat=self.lat,
                lng=self.lng,
                tz_str=self.tz_str,
                geonames_username=geonames_username
            )
        except Exception as e:
            import traceback
            self.error = f"{e}\n{traceback.format_exc()}"
            self.chart = None

    def get_planetary_positions(self):
        if self.chart:
            # Collect all planet attributes
            planets = [
                self.chart.sun,
                self.chart.moon,
                self.chart.mercury,
                self.chart.venus,
                self.chart.mars,
                self.chart.jupiter,
                self.chart.saturn,
                self.chart.uranus,
                self.chart.neptune,
                self.chart.pluto,
                self.chart.mean_node,
                self.chart.true_node,
                self.chart.mean_south_node,
                self.chart.true_south_node
            ]
            # Optionally add chiron and lilith if present
            if getattr(self.chart, "chiron", None):
                planets.append(self.chart.chiron)
            if getattr(self.chart, "mean_lilith", None):
                planets.append(self.chart.mean_lilith)
            return planets
        return None

    def get_house_cusps(self):
        if self.chart:
            houses = [
                self.chart.first_house,
                self.chart.second_house,
                self.chart.third_house,
                self.chart.fourth_house,
                self.chart.fifth_house,
                self.chart.sixth_house,
                self.chart.seventh_house,
                self.chart.eighth_house,
                self.chart.ninth_house,
                self.chart.tenth_house,
                self.chart.eleventh_house,
                self.chart.twelfth_house
            ]
            return houses
        return None

    def validate(self):
        if self.error:
            return False, self.error
        return True, None