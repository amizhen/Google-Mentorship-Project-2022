
class PowerSys:
    def __init__(self, amt_solar, amt_wind, amt_storage):
        self.storage = amt_storage
        self.wind = amt_wind
        self.solar = amt_solar

    def __str__(self):
        return f'({self.solar}, {self.wind}, {self.storage})'

if __name__ == '__main__':
    a = PowerSys(1, 2, 3)
    print(a)
    print(a.storage)