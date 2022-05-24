from util.Formula import get_wind_power, get_solar_power
from datetime import datetime

class PowerSys:
    def __init__(self, amt_solar, amt_wind, amt_storage):
        self.storage_cap = amt_storage
        self.stored = amt_storage
        self.wind = amt_wind
        self.solar = amt_solar
        self.fitness = 0


        # Data for fitness functions
        self.net_history = {} # Chart of time vs net_generated
        # format = time:net
        self.storage_history = {}  # Chart of time vs amt of power in storage, shows deficit for the hour if negative
        # format = time:storage
        self.gen_history = {}  # Chart of time vs power generated at that time
        # format = time:(wind, solar)
        self.waste_history = {} # Chart of time vs excess generated power that could not be stored.
        # format = time:waste



    def hour_tick(self, wind_power : float, solar_power : float, demand : float, time : datetime):
        net_energy = wind_power * self.wind + solar_power * self.solar - demand

        self.waste_history[time] = max(0,  self.stored + net_energy - self.storage_cap)
        self.net_history[time] = net_energy

        self.stored = min(self.storage_cap, self.stored+net_energy)

        self.storage_history[time] = self.stored

        self.stored = max(self.stored, 0)



    def calc_fitness(self):
        hours_blackout = 0
        total_gap = 0.0
        total_waste = 0.0
        for time in self.storage_history.keys():
            if self.storage_history[time] < 0:
                total_gap += self.storage_history[time]
                hours_blackout += 1
                self.fitness -= self.storage_history[time] / 100 # Weights for fitness should be changed
                self.fitness -= 1 # Weights for fitness should be changed
            else:
                total_waste += self.waste_history[time]
                self.fitness -= self.waste_history[time] / 1000 # Weights for fitness should be changed


    def __str__(self):
        return f'({self.solar}, {self.wind}, {self.storage_cap}'

    # Makes PowerSys sortable by the fitness score

    def __eq__(self, other : 'PowerSys'):
        return self.fitness == other.fitness

    def __lt__(self, other : 'PowerSys'):
        return self.fitness < other.fitness

    def __ne__(self, other : 'PowerSys'):
        return not self.__eq__(other)

    def __gt__(self, other : 'PowerSys'):
        return other.__lt__(other)

    def __ge__(self, other : 'PowerSys'):
        return not self.__lt__(other)

    def __le__(self, other : 'PowerSys'):
        return other.__ge__(self)

if __name__ == '__main__':
    a = PowerSys(1, 2, 3)
    print(a)
    print(a.stored)
