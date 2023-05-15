import os
from math import sqrt
import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.wkt import loads
import csv

class OilTerminals:
    """Class method for oil terminals data"""
    terminal_file_path = 'data/uk_oil_terminals.xlsx'
    assert os.path.exists(terminal_file_path) is True
    
    @staticmethod
    def bounding_box(
            center_lat: np.float64 = None,          
            center_lon: np.float64 = None, 
            half_side: np.int64 = 10, # in Km
            ):
        """
        Function that gives WKT of a polygon from a center lon, lat

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

        # Geopandas geo-series
        gs = gpd.GeoSeries(loads(f'POINT({center_lon} {center_lat})'))
        # GeoDataFrame
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

    def __init__(self) -> None:
        """Declaring variables"""
        pass

    def read_data(self):
        """Read data from xlsx file"""
        # Load the excel file
        df = pd.read_excel(
            self.terminal_file_path, 
            skiprows = 1)

        # Lat, lon list
        lat_lon = list(zip(df['Lat'], df['Lon']))

        # create a dictionary of of lat lon with location names
        self.terminal_dict = {}
        self.terminal_bbox = {}
        for index, row in df.iterrows():
            location = row['Region']
            location = location.split(',')[0].lower()
            self.terminal_dict[location] = lat_lon[index]

            # Getting the bounding box coords
            wkt = OilTerminals.bounding_box(
                center_lat = lat_lon[index][0],
                center_lon = lat_lon[index][1])
            polygon = loads(wkt)
            vertices = list(polygon.exterior.coords)
            self.terminal_bbox[location] = vertices

        return self.terminal_dict
    
    def write_csv(
            self,
            filepath:str = None)-> None:
        """Writing CSV files with bounding box"""
        with open(filepath, mode = 'w', newline = '') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['location', 'bounding_coords'])
            for key , value in self.terminal_bbox.items():
                writer.writerow([key, value])
            csvfile.close()
        
        


         

