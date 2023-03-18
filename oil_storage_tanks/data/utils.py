import ee
import os
import math
import numpy as np
import pandas as pd
from shapely.geometry import Polygon
from shapely.wkt import dumps
import json
from oil_storage_tanks.utils import logger
from google.auth.transport.requests import AuthorizedSession
from google.oauth2 import service_account

# Getting the logger function
log = logger()

def ee_authenticate(
        service_acc_key: str
        ):
    """Authenticating Earth Engine

    Args:
        service_acc_key: Path to the service account key JSON file
    """
    # Reading the credentials
    log.info("Reading the credentials from the service key json file")
    credentials = service_account.Credentials.from_service_account_file(service_acc_key)
    scoped_credentials = credentials.with_scopes(
        ['https://www.googleapis.com/auth/cloud-platform'])

    session = AuthorizedSession(scoped_credentials)

    url = 'https://earthengine.googleapis.com/v1alpha/projects/earthengine-public/assets/LANDSAT'
    
    log.info("Starting the session for authentication")
    response = session.get(url)
    json_format = json.loads(response.content)
    if json_format is not None:
        log.info("Authentication successful!")
    return json_format

def ee_initiate(
        service_account: str = 'storage-tank@gy7720.iam.gserviceaccount.com',
        private_key:str = None
        )-> None:
    """
    Function to authenticate Earth Engine

    Args:
        service_account: Name of the service account
        private_key: Path to the downloaded service account private key
    """
    credentials = ee.ServiceAccountCredentials(service_account, private_key)

    ee.Initialize(credentials)

    log.info("Earth Engine Initiation successful!")


def bounding_box(
        center_lat: np.float64, 
        center_lon: np.float64, 
        half_side: np.int64 = 50):
    """
    Function that gives WKT of a polygin from a center lon, lat

    Args:
        center_lat: Centre Latitude
        center_lon: Center Longitude
        half_side: Length from center to side of the bounding ox in Km
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

def oil_terminals(
        terminal_file_path: str
        ):
    """
    Function to get the lat, lon of oi termianls

    Args:
        terminal_file_path: File path to terminal information
    """
    # Load the csv file
    log.info(f"Reading the xlsx file:{terminal_file_path}")
    df = pd.read_excel(
        terminal_file_path, 
        skiprows = 1)

    # Lat, lon list
    lat_lon = list(zip(df['Lat'], df['Lon']))

    # create a dictionary of of lat lon with location names
    terminal_dict = {}
    for index, row in df.iterrows():
        terminal_dict[row['Name']] = lat_lon[index]
    if terminal_dict is not None:
        log.info("Reading the xlsx file is successful!")
    return terminal_dict

