"""
HSDS data extraction functions
@author See https://github.com/NREL/hsds-examples
"""
import numpy as np
from pyproj import Proj


def WTK_idx(wtk, lat_lon):
    """
    Function to find the nearest x/y WTK indices for a given lat/lon using
    Proj4 projection library

    Parameters
    ----------
    wtk : 'h5pyd.File'
        h5pyd File instance for the WTK
    lat_lon : tuple | list
        (lat, lon) coordinates of interest

    Results
    -------
    ij : 'tuple'
        x/y coordinate in the database of the closest pixel to coordinate of
        interest
    """
    dset_coords = wtk['coordinates']
    projstring = """+proj=lcc +lat_1=30 +lat_2=60
                    +lat_0=38.47240422490422 +lon_0=-96.0
                    +x_0=0 +y_0=0 +ellps=sphere
                    +units=m +no_defs """
    projectLcc = Proj(projstring)
    # Grab origin directly from database
    origin_ll = reversed(dset_coords[0][0])
    origin = projectLcc(*origin_ll)

    lon_lat = reversed(lat_lon)
    coords = projectLcc(*lon_lat)
    delta = np.subtract(coords, origin)
    ij = [int(round(x / 2000)) for x in delta]
    return tuple(reversed(ij))
