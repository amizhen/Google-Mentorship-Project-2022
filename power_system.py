from datetime import datetime, timedelta
from power_plant import WindPlant, SolarPlant
from combined_data import get_demand
from pprint import pprint


class PowerSys:
    def __init__(self, region: str, amt_storage: float, start: datetime, end: datetime, percentSatisfied  : float = 1.0):
        self.fitness = 0
        self.STORAGECAP = amt_storage
        self.stored = 0 # amt_storage
        self.wind_plants = []
        self.solar_plants = []
        self.start = start
        self.end = end
        self.region = region
        self.demand = self.fetch_data()
        self.percentSatisfied = percentSatisfied

        # Data for fitness functions
        self.net_history = {}  # Chart of time vs net_generated
        # format = time:net
        self.storage_history = {}  # Chart of time vs amt of power in storage, shows deficit for the hour if negative
        # format = time:storage
        self.gen_history = {}  # Chart of time vs power generated at that time
        # format = time:[wind, solar]
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
        self.gen_history[time] = [0, 0]
        net = -self.demand[time] * self.percentSatisfied
        for turbine in self.wind_plants:
            net += turbine.tick(time)
            self.gen_history[time][1] += turbine.tick(time)
        for solar in self.solar_plants:
            net += solar.tick(time)
            self.gen_history[time][0] += solar.tick(time)

        self.net_history[time] = net
        # print(self.stored, net, self.demand[time], sum(self.gen_history[time]))
        if self.stored + net < 0:
            self.storage_history[time] = self.stored + net
            self.stored = 0
        else:
            if self.stored + net > self.STORAGECAP:
                self.waste_history[time] = self.stored + net - self.STORAGECAP
            self.stored = min(net+self.stored, self.STORAGECAP)
            self.storage_history[time] = self.stored

    # def calc_fitness(self): NOT NECESSARY SINCE WE ARE NO LONGER OPTIMISING
    #     hours_blackout = 0
    #     total_gap = 0.0
    #     total_waste = 0.0
    #     for time in self.storage_history.keys():
    #         if self.storage_history[time] < 0:
    #             total_gap += self.storage_history[time]
    #             hours_blackout += 1
    #             self.fitness -= self.storage_history[time] / 100  # Weights for fitness should be changed
    #             self.fitness -= 1  # Weights for fitness should be changed
    #         else:
    #             total_waste += self.waste_history[time]
    #             self.fitness -= self.waste_history[time] / 1000  # Weights for fitness should be changed

    def run(self) -> None:
        diff_hours = int((self.end - self.start).total_seconds() / 3600)
        for diff in range(diff_hours):
            time = self.start + timedelta(hours=diff)
            self.tick(time)


    def calc_needed_storage(self):
        out = 0
        count = 0
        for time in self.storage_history:
            if self.storage_history[time] > 0 and count > 0:
                out = max(count, out)
                count = 0
            elif self.storage_history[time] < 0:
                count += self.storage_history[time] * -1
        out = max(count, out)
        return out


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
    syst = PowerSys("New York", 20000, datetime(2016, 1, 1), datetime(2017, 1, 1))
    syst.add_solar((42.77376799574172, -75.0433619493047), 250000000)
    syst.add_wind((42.77376799574172, -75.0433619493047), 10000)
    syst.run()
    for i in range(len(syst.storage_history)):
        print(list(syst.gen_history.keys())[i], list(syst.gen_history.values())[i], list(syst.demand.values())[i], list(syst.storage_history.values())[i] )

    print(syst.calc_needed_storage())

