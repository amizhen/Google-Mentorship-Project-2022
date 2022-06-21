from combined_data import get_solar, get_wind
from datetime import datetime


class PowerPlant:
    def __init__(self, location: tuple[float, float], amount: float, start: datetime, end: datetime):
        self.loc = location
        self.amt = amount
        self.start = start
        self.end = end
        self.data = self.fetch_data()

    def tick(self, time: datetime):
        return self.process_data(time)

    def fetch_data(self):
        return NotImplemented

    def process_data(self, time: datetime):
        return self.data[time] * self.amt

    def __str__(self):
        return NotImplemented


class WindPlant(PowerPlant):
    def __init__(self, location: tuple[float, float], amount: int, start: datetime, end: datetime, radius=35.0,
                 height=80.0):
        self.radius = radius
        self.height = height
        super().__init__(location, amount, start, end)

    def fetch_data(self):
        return get_wind(self.start, self.end, self.loc[0], self.loc[1], self.radius, self.height)


class SolarPlant(PowerPlant):
    def __init__(self, location: tuple[float, float], amount: float, start: datetime, end: datetime, efficiency=0.15):
        self.efficiency = efficiency
        super().__init__(location, amount, start, end)

    def fetch_data(self):
        return get_solar(self.start, self.end, self.loc[0], self.loc[1], self.efficiency)


if __name__ == '__main__':
    pass
