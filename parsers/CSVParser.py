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

    def __init__(self, filePath : str, *args : list[str]):
        self._filePath = filePath
        self._csvFile = open(filePath, "r")
        self._opened = True
        self._reader = csv.DictReader(self._csvFile)
        self._categories = [arg for arg in args if arg in self._reader.fieldnames]

    def __call__(self) -> list[Mapping[str, str]]:
        if not self._categories:
            print("stff") # TODO: throw exception
        if self._opened:
            data = []
            for row in self._reader:
                rowData = {category : row[category] for category in self._categories}
                if rowData:
                    data.append(rowData)
            return data

    def addCategory(self, *args : list[str]) -> None:
        for category in args:
            if isinstance(category, str) and category not in self._categories and category in self._reader.fieldnames:
                self._categories.append(category)

    def removeCategory(self, *args : list[str]) -> None:
        for category in args:
            if isinstance(category, str) and category in self._categories and category in self._reader.fieldnames:
                self._categories.remove(category)

    def clearCategory(self) -> None:
        self._categories.clear();

    def close(self) -> None :
        self._csvFile.close()
        self._opened = False

if __name__ == "__main__":
    print(CSVParser("data\\raw\\csv\\biomass.csv", "lat", "lon")())