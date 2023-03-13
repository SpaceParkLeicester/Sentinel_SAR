import ee
import logging
import math
import numpy as np
from shapely.geometry import Polygon
from shapely.wkt import dumps
import json
import asf_search as asf

log = logging.getLogger(__name__)

def ee_initiate(
        service_account: str = 'storage-tank@gy7720.iam.gserviceaccount.com',
        private_key:str = None
        )-> None:
    """Function to authenticate Earth Engine

        service_account = Name of the service account
        private_key = Path to the downloaded service account private key
    """
    credentials = ee.ServiceAccountCredentials(service_account, private_key)

    ee.Initialize(credentials)

    log.info("Earth Engine Initiation successful")


def bounding_box(
        center_lat: np.float64, 
        center_lon: np.float64, 
        half_side: np.int64):
    """Function that gives WKT of a polygin from a center lon, lat

        center_lat = Centre Latitude
        center_lon = Center Longitude
        half_side = Length from center to side of the bounding ox in Km
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

    # Convert the polygon object to WKT string
    return dumps(poly)

def earthdata_authentication(
        cred_file_path: str
        ):
    """Function to authenticate Eartdata login
        cred_file_path = Path to the credential file
    """
    # Opening the credential file and reading the data
    with open(cred_file_path, "r") as f:
        data = json.load(f)
        username = data.username
        password = data.password
        session = asf.ASFSession().auth_with_creds(username, password)
        f.close()
    
    return session


