import pprint
import xml.etree.ElementTree as ET;
import re
import sys

"""
Notes:

kml files are xml files

Should use xpath to parse through the kml tree
Look at kml/Document/Folder/Placemark/LookAt for general coordinates
Look at kml/Document/Folder/Placemark/name for ID of the item
Look at kml/Document/Folder/Placemark/description for data

We could extract the COORDINATES, the NAME, and the DATA.
We can append these to the corresponding csv files (to make smaller files with the data)

We could probably create our own csv file instead of modifying existing ones because it will be simpler.
The drawback of this method is that we have to parse through the html in description which might be painful (Could tackle it using regex and capture groups)

OR

We could only take the Coordinates and Name and modify existing csv files

kml files we need to process are in data/raw/kml
"""

filePath = r"data\raw\kml\biomass.kml"

tree = ET.parse(filePath)
root = tree.getroot()

namespaces = {
    "":"http://www.opengis.net/kml/2.2"
}

pattern = re.compile('"atr-name">(\w*).*"atr-value">(\w*)<')

state = True;

if __name__ == "__main__":

    file = f"data\\raw\\kml\\{sys.argv[1]}.kml"
    with open(f"data\\processed\\{sys.argv[1]}.csv", "w") as file:
        
        line = root.find("./Document/Folder/Placemark/description").text

        for placemark in root.findall("./Document/Folder/Placemark", namespaces=namespaces):
            data = {}

            placemarkID = placemark.find("./name", namespaces=namespaces).text

            long = placemark.find("./LookAt/longitude", namespaces=namespaces).text
            lat = placemark.find("./LookAt/latitude", namespaces=namespaces).text
            
            for match in pattern.finditer(placemark.find("./description", namespaces=namespaces).text):
                data |= {match.group(1) : match.group(2)}

    with open(f"data\\processed\\{file}.csv", "w") as file:
        firstLine = "FID,lat,lon"
        for key in data.keys():
            firstLine += "," + key
        file.write(key)