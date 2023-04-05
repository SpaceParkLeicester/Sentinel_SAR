import math
import numpy as np
import pandas as pd
from shapely.wkt import dumps
from shapely.geometry import Polygon
from .log import logger
from typing import Optional

def bounding_box(
        center_lat: np.float64 = 58.83834793,          
        center_lon: np.float64 = -3.121350468, 
        half_side: np.int64 = 100,
        just_coords: Optional[bool] = False):
    """
    Function that gives WKT of a polygin from a center lon, lat

    Args:
        center_lat: Centre Latitude
        center_lon: Center Longitude
        half_side: Length from center to side of the bounding box in Km.
        just_coords: If True, gives the list of four corner corrdinates.
    """
    # Sanity check
    assert half_side > 0
    assert center_lat >= -90.0 and center_lat  <= 90.0
    assert center_lon >= -180.0 and center_lon <= 180.0

    # Convert degrees to radians
    lat = math.radians(center_lat)
    lon = math.radians(center_lon)

    # Earth radius in km
    RADIUS = 6371

    # Radius of the parallel at given latitude
    parallel_radius = RADIUS * math.cos(lat)

    # Angular distance in radians on a great circle
    ang_dist = half_side / RADIUS

    # Minimum and maximum latitudes for given distance
    lat_min = lat - ang_dist
    lat_max = lat + ang_dist

    # Minimum and maximum longitudes for given distance
    lon_min = lon - ang_dist / parallel_radius
    lon_max = lon + ang_dist / parallel_radius

    # Convert radians back to degrees
    rad2deg = math.degrees

    # Create a list of coordinates as tuples
    coords = [
        (rad2deg(lon_min), rad2deg(lat_min)), 
        (rad2deg(lon_max), rad2deg(lat_min)), 
        (rad2deg(lon_max), rad2deg(lat_max)), 
        (rad2deg(lon_min), rad2deg(lat_max))
        ]
    # Create a polygon object from the coordinates
    poly = Polygon(coords)

    if just_coords:
        return coords
    else:
        # Convert the polygon object to WKT string
        return dumps(poly)

def oil_terminals(
        terminal_file_path: str,
        log = logger()
        ):
    """
    Function to get the lat, lon of oi termianls

    Args:
        terminal_file_path: File path to terminal information
    """
    # Load the csv file
    df = pd.read_excel(
        terminal_file_path, 
        skiprows = 1)

    # Lat, lon list
    lat_lon = list(zip(df['Lat'], df['Lon']))

    # create a dictionary of of lat lon with location names
    terminal_dict = {}
    for index, row in df.iterrows():
        terminal_dict[row['Name']] = lat_lon[index]
    return terminal_dict

         