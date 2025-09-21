# views/astrology_chart_view.py
from entities.astrology_chart import AstrologyChartEntity

class AstrologyChartView:
    def __init__(self, **kwargs):
        self.entity = AstrologyChartEntity(**kwargs)
        self.display()

    def display(self):
        valid, error = self.entity.validate()
        if not valid:
            self.show_error(error)
        else:
            self.show_chart()

    def show_chart(self):
        planetary_positions = self.entity.get_planetary_positions()
        house_cusps = self.entity.get_house_cusps()
        print("Planetary Positions:")
        if planetary_positions:
            for planet in planetary_positions:
                print(planet)
        else:
            print("No planetary positions found.")
        print("House Cusps:")
        if house_cusps:
            for house in house_cusps:
                print(house)
        else:
            print("No house cusps found.")

    def show_error(self, error):
        print(f"Error generating chart:\n{error}")