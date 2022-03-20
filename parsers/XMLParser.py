import xml.etree.ElementTree as ET;

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

if __name__ == "__main__":
    print(tree.getroot().tag)