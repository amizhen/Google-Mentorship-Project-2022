from datetime import datetime
from combined_data import *


class PowerSys:
    def __int__(self, region, amt_storage):
        self.fitness = 0
        self.storage_cap = amt_storage
        self.stored = amt_storage
        self.wind_plants = []
        self.solar_plants = []
        self.demand = self.get_data()

        # Data for fitness functions
        self.net_history = {}  # Chart of time vs net_generated
        # format = time:net
        self.storage_history = {}  # Chart of time vs amt of power in storage, shows deficit for the hour if negative
        # format = time:storage
        self.gen_history = {}  # Chart of time vs power generated at that time
        # format = time:(wind, solar)
        self.waste_history = {}  # Chart of time vs excess generated power that could not be stored.
        # format = time:waste

    def get_data(self):
        return NotImplemented
        # API call for usage data

    def tick(self, time):
        self.gen_history[time] = (0, 0)

        net = -1 * self.demand[time]
        for turbine in self.wind_plants:
            net += turbine.tick(time)
            self.gen_history[time][0] += turbine.tick(time)
        for solar in self.solar_plants:
            net += solar.tick(time)
            self.gen_history[time][0] += solar.tick(time)

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


class PowerPlant:
    def __init__(self, location, amount, start, end, mode=None):
        self.loc = location
        self.amt = amount
        self.mode = mode
        self.start = start
        self.end = end
        self.data = self.fetch_data()

    def tick(self, time):
        return self.processData(time)

    def fetch_data(self):
        return NotImplemented

    def processData(self, time):
        return self.data[time] * self.amt

    def __str__(self):
        return f'{self.amt}, {self.mode} at {self.loc}'


class WindPlant(PowerPlant):
    def __init__(self, location, amount, start, end, radius=35, height=80):
        super().__init__(location, amount, start, end, mode='wind')
        self.radius = radius
        self.height = height

    def fetch_data(self):
        return get_wind(self.start, self.end, self.loc[0], self.loc[1], self.radius, self.height)


class SolarPlant(PowerPlant):
    def __init__(self, location, amount, start, end, efficiency=0.15):
        super().__init__(location, amount, start, end, mode='solar')
        self.efficiency = efficiency

    def fetch_data(self):
        return get_solar(self.start, self.end, self.loc[0], self.loc[1], self.efficiency)


# if __name__ == '__main__':
    # a = PowerSys(1, 2, 3)
    # print(a)
    # print(a.stored)
