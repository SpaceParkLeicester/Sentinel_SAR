from math import sqrt
import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.wkt import dumps, loads
from shapely.geometry import Polygon
from typing import Optional

def bounding_box(
        center_lat: np.float64 = 58.83834793,          
        center_lon: np.float64 = -3.121350468, 
        half_side: np.int64 = 100, # in Km
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

    # Km to m
    half_side = (half_side*1000)/sqrt(2)

    # Geopandas geoseries
    gs = gpd.GeoSeries(loads(f'POINT({center_lon} {center_lat})'))
    # GeoDataframe
    gdf = gpd.GeoDataFrame(geometry=gs)
    # Projection
    gdf.crs='EPSG:4326'
    gdf = gdf.to_crs('EPSG:3857')
    res = gdf.buffer(
        distance=half_side,
        cap_style=3,
    )    

    # Get the geom
    geom = res.to_crs('EPSG:4326').iloc[0]
    # Getting Polygon WKT string
    return geom.wkt

def oil_terminals(terminal_file_path: str):
    """Function to get the lat, lon of oil termianls

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
        location = row['Region']
        location = location.split(',')[0].lower()
        terminal_dict[location] = lat_lon[index]
    return terminal_dict

def polygon_coords_csv(
        terminal_file_path:str = None,
        half_side:np.int64 = None,
        out_csv_file:str = None):
    """Writing polygon bounding box coords"""
    # Load the csv file
    df = pd.read_excel(
        terminal_file_path, 
        skiprows = 1)
    
    # Getting the bbox
    polygon_wkt = []
    for row, _ in df.iterrows():
        center_coords_lat = df['Lat'][row]
        center_coords_lon = df['Lon'][row]
        poly_wkt = bounding_box(
            center_lat = center_coords_lat,
            center_lon = center_coords_lon,
            half_side = half_side)
        polygon_wkt.append(poly_wkt)
    df['Polygon'] = polygon_wkt
    return df
        