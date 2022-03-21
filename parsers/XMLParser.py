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

"""
Usage - python XMLParser.py {insert kml file name without extension}
"""
if __name__ == "__main__":
    ns = {"":"http://www.opengis.net/kml/2.2"}
    pattern = re.compile('"atr-name">([\w.-/\s]*).*"atr-value">([-\w./\s]*)<')
    fileKml = f"data\\raw\\kml\\{sys.argv[1]}.kml"

    includeCoord = bool(sys.argv[2])

    tree = ET.parse(fileKml)
    root = tree.getroot()

    with open(f"data\\processed\\{sys.argv[1]}.csv", "w") as file:

        # firstLine = "FID,lat,lon"
        firstLine = "FID"
        line = root.find("./Document/Folder/Placemark/description", namespaces=ns).text
        keys = []
        for match in pattern.finditer(line):
            firstLine += "," + match.group(1)
            keys.append(match.group(1))

        file.write(firstLine + "\n");

        for placemark in root.findall("./Document/Folder/Placemark", namespaces=ns):
            data = dict.fromkeys(keys)

            placemarkID = placemark.find("./name", namespaces=ns).text

            #long = placemark.find("./LookAt/longitude", namespaces=ns).text
            #lat = placemark.find("./LookAt/latitude", namespaces=ns).text
            
            for match in pattern.finditer(placemark.find("./description", namespaces=ns).text):
                data[match.group(1)] = match.group(2)

            # dataLine = f"{placemarkID},{lat},{long}"
            dataLine = f"{placemarkID}"
            for key in data:
                dataLine += "," + (data[key] if data[key] != None else "")
            dataLine+="\n"
            file.write(dataLine)