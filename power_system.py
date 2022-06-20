from datetime import datetime, timedelta
from power_plant import WindPlant, SolarPlant
from combined_data import get_demand


class PowerSys:
    def __init__(self, region: str, amt_storage: float, start: datetime, end: datetime):
        self.fitness = 0
        self.storage_cap = amt_storage
        self.stored = amt_storage
        self.wind_plants = []
        self.solar_plants = []
        self.start = start
        self.end = end
        self.region = region
        self.demand = self.fetch_data()

        # Data for fitness functions
        self.net_history = {}  # Chart of time vs net_generated
        # format = time:net
        self.storage_history = {}  # Chart of time vs amt of power in storage, shows deficit for the hour if negative
        # format = time:storage
        self.gen_history = {}  # Chart of time vs power generated at that time
        # format = time:(wind, solar)
        self.waste_history = {}  # Chart of time vs excess generated power that could not be stored.
        # format = time:waste

    def set_region(self, region : str):
        self.region = region
        self.demand = self.fetch_data()

    def add_wind(self, loc: tuple[float, float], amt: int, radius: float = 35.0, height: float = 80):
        try:
            self.wind_plants.append(WindPlant(loc, amt, self.start, self.end, radius=radius, height=height))
        except:
            pass

    def add_solar(self, loc: tuple[float, float], amt: float, efficancy: float = 0.15):
        try:
            self.solar_plants.append(SolarPlant(loc, amt, self.start, self.end, efficiency=efficancy))
        except:
            pass

    def fetch_data(self):
        return get_demand(self.start, self.end, self.region)
        # API call for usage data

    def tick(self, time: datetime):
        self.gen_history[time] = 0

        net = -1 * self.demand[time]
        for turbine in self.wind_plants:
            net += turbine.tick(time)
            self.gen_history[time] += turbine.tick(time)
        for solar in self.solar_plants:
            net += solar.tick(time)
            self.gen_history[time] += solar.tick(time)

        self.net_history[time] = net

        if self.stored + net > self.storage_cap:
            self.waste_history[time] = self.stored + net - self.storage_cap

        if self.stored + net < 0:
            self.storage_history[time] = self.stored + net
            self.stored = 0
        else:
            self.stored += net
            self.storage_history[time] = self.stored

    def calc_fitness(self):
        hours_blackout = 0
        total_gap = 0.0
        total_waste = 0.0
        for time in self.storage_history.keys():
            if self.storage_history[time] < 0:
                total_gap += self.storage_history[time]
                hours_blackout += 1
                self.fitness -= self.storage_history[time] / 100  # Weights for fitness should be changed
                self.fitness -= 1  # Weights for fitness should be changed
            else:
                total_waste += self.waste_history[time]
                self.fitness -= self.waste_history[time] / 1000  # Weights for fitness should be changed

    def run(self) -> None:
        diff_hours = int((self.end - self.start).total_seconds() / 3600)
        for diff in range(diff_hours):
            time = self.start + timedelta(hours=diff)
            self.tick(time)

    # Makes PowerSys sortable by the fitness score

    def __eq__(self, other: 'PowerSys'):
        return self.fitness == other.fitness

    def __lt__(self, other: 'PowerSys'):
        return self.fitness < other.fitness

    def __ne__(self, other: 'PowerSys'):
        return not self.__eq__(other)

    def __gt__(self, other: 'PowerSys'):
        return other.__lt__(other)

    def __ge__(self, other: 'PowerSys'):
        return not self.__lt__(other)

    def __le__(self, other: 'PowerSys'):
        return other.__ge__(self)


if __name__ == '__main__':
    pass
