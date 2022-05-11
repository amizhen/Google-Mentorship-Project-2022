class PowerSys:
    def __init__(self, amt_solar, amt_wind, amt_storage):
        self.storage_cap = amt_storage
        self.stored = amt_storage
        self.wind = amt_wind
        self.solar = amt_solar
        self.fitness = 0
        self.gen_history = {}  # Chart of time vs power generated at that time
        # format = time:(wind, solar)
        self.storage_history = {}  # Chart of time vs amt of power in storage, shows deficit for the hour if negative
        # format = time:net

    def __str__(self):
        return f'({self.solar}, {self.wind}, {self.storage_cap}'

    # Makes PowerSys sortable by the fitness score

    def __eq__(self, other : "PowerSys"):
        return self.fitness == other.fitness

    def __lt__(self, other : "PowerSys"):
        return self.fitness < other.fitness

    def __ne__(self, other : "PowerSys"):
        return not self.__eq__(other)

    def __gt__(self, other : "PowerSys"):
        return other.__lt__(other)

    def __ge__(self, other : "PowerSys"):
        return not self.__lt__(other)

    def __le__(self, other : "PowerSys"):
        return other.__ge__(self)

if __name__ == '__main__':
    a = PowerSys(1, 2, 3)
    print(a)
    print(a.stored)
