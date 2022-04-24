class PowerSys:
    def __init__(self, amt_solar, amt_wind, amt_storage):
        self.storage = amt_storage
        self.wind = amt_wind
        self.solar = amt_solar
        self.fitness = 0

    def __str__(self):
        return f'({self.solar}, {self.wind}, {self.storage}, {self.fitness})'

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __le__(self, other):
        return self.fitness <= other.fitness

    def __eq__(self, other):
        return self.fitness == other.fitness

    def __ne__(self, other):
        return self.fitness != other.fitnes

    def __gt__(self, other):
        return self.fitness > other.fitness

    def __ge__(self, other):
        return self.fitness >= other.fitness


if __name__ == '__main__':
    a = PowerSys(1, 2, 3)
    print(a)
    print(a.storage)
