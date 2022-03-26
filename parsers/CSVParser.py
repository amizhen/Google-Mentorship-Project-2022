import csv
import re
from typing import Mapping

from util.Filters import Filter 

def check_int(str):
    return re.match(r"[-+]?\d+(\0*)?$", str) != None

def check_float(str):
    return re.match(r'^[-+]?\d+(?:\.\d+)$', str) != None

class CSVParser:

    def __init__(self, filePath : str, *categories : list[str]):
        self._filePath = filePath
        self._csvFile = open(filePath, "r")
        self._opened = True
        self._reader = csv.DictReader(self._csvFile)
        self._categories = [arg for arg in categories if arg in self._reader.fieldnames]
        
    def __call__(self) -> list[Mapping[str, str]]:
        if not self._categories:
            self._categories = self._reader.fieldnames
        if self._opened:
            data = []
            for row in self._reader:
                rowData = {}
                for category in self._categories:
                    val = row[category]
                    if check_int(val):
                        val = int(val)
                    elif check_float(val):
                        val = float(val)
                    rowData |= {category : val}
                if rowData:
                    data.append(rowData)
            return data

    def addCategory(self, *categories : list[str]) -> None:
        for category in categories:
            if isinstance(category, str) and category not in self._categories and category in self._reader.fieldnames:
                self._categories.append(category)

    def removeCategory(self, *categories : list[str]) -> None:
        for category in categories:
            if isinstance(category, str) and category in self._categories and category in self._reader.fieldnames:
                self._categories.remove(category)

    def clearCategory(self) -> None:
        self._categories.clear()

    def close(self) -> None :
        self._csvFile.close()
        self._opened = False

if __name__ == "__main__":
    @Filter(lambda data : data["lat"] < 32)
    def getData():
        return CSVParser("data\\raw\\csv\\biomass.csv", "lat", "lon")()

    file = open("data\\raw\\csv\\biomass.csv", "r")
    @Filter.less_than("lat", 33)
    @Filter.in_range_exclusive("lon", -110, -100)
    def getData2():
        return csv.DictReader(file)

    print(getData2())
    file.close()