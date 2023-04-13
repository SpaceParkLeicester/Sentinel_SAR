from math import sqrt
import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.wkt import dumps, loads
from shapely.geometry import Polygon
from typing import Optional

class OilTerminals:
    """Class method for oil terminals data"""
    file_path = 'data/uk_oil_terminals.xlsx'
    
    @staticmethod
    def bounding_box(
            center_lat: np.float64 = 58.83834793,          
            center_lon: np.float64 = -3.121350468, 
            half_side: np.int64 = 100, # in Km
            ):
        """
        Function that gives WKT of a polygin from a center lon, lat

        Args:
            center_lat: Centre Latitude
            center_lon: Center Longitude
            half_side: Length from center to side of the bounding box in Km.
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

    def __init__(
            self,
            terminal_file_path:str = 'data/uk_oil_terminals.xlsx',
            location_name:str = None,
            half_side:np.int64 =None) -> None:
        """Declaring variables"""
        self.terminal_file_path = terminal_file_path
        self.location_name = location_name
        self.half_side = half_side

    def read_data(self):
        """Read data from xlsx file"""
        # Load the csv file
        df = pd.read_excel(
            self.terminal_file_path, 
            skiprows = 1)

        # Lat, lon list
        lat_lon = list(zip(df['Lat'], df['Lon']))

        # create a dictionary of of lat lon with location names
        self.terminal_dict = {}
        for index, row in df.iterrows():
            location = row['Region']
            location = location.split(',')[0].lower()
            self.terminal_dict[location] = lat_lon[index]
        return self.terminal_dict

    def polygon_coords(self):
        """Getting polygon wkt for the bounding box"""
        # Getting the bbox
        polygon_wkt = []
        for loc, coords in self.terminal_dict.items():
            if loc == self.location_name:
                center_lat = coords[0]
                center_lon = coords[1]
                poly_wkt = OilTerminals.bounding_box(
                    center_lat = center_lat,
                    center_lon = center_lon,
                    half_side = self.half_side)
                return poly_wkt
            else:
                return None
        