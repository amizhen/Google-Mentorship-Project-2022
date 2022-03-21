import csv
from typing import Mapping

"""
Notes:

Our life is a lot easier here because we have our data has coordinates.

We should just figure out how to parse through all of this data. This is like step 2 after we process kml files and create or modify the csv files.

CSV FILES THAT I LOVE AND ADMIRE - wave_energy.csv

CSV FILES THAT WE NEED TO FIX - the rest
"""

filePath = open("data\\raw\\csv\\biomass.csv")

file = csv.DictReader(filePath)

class CSVParser:

    def __init__(self, filePath : str):
        self.filePath = filePath
        self.csvFile = open(filePath, "r")
        self.opened = True
        self.categories = []

    def __call__(self) -> list[Mapping[str, str]]:
        if self.opened:
            print(self.filePath)
            print(self.categories)
            reader = csv.DictReader(self.csvFile)
            reader.fieldnames
        # return [{key : row[key] for key in row} for row in reader] # TODO: Fix the dict comprehension

    def addCategory(self, *args : list[str]) -> None:
        for category in args:
            if isinstance(category, str) and category not in self.categories:
                self.categories.append(category)

    def removeCategory(self, *args : list[str]) -> None:
        for category in args:
            if isinstance(category, str) and category in self.categories:
                self.categories.remove(category)

    def clearCategory(self) -> None:
        self.categories.clear();

    def close(self) -> None :
    
        self.csvFile.close()
        self.opened = False


if __name__ == "__main__":
    parser = CSVParser("data\\raw\\csv\\biomass.csv")
    parser.addCategory("Lat")

    parser()