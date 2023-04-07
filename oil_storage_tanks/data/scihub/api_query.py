import os
import numpy as np
import pandas as pd
from shapely.wkt import loads

from oil_storage_tanks.data import auth_credentials, oil_terminals
from oil_storage_tanks.data import bounding_box as bbox
from oil_storage_tanks.utils import stitch_strings

class search_data(auth_credentials):
    """Functions to search data in scihub"""
    def __init__(
            self, 
            data_service: str = None, 
            path_to_cred_file: str = None,
            username:str = None,
            password:str = None,
            log=None) -> None:
        super().__init__(
            data_service, 
            path_to_cred_file, 
            username, password, log)
        self.api = super().scihub_auth()
    
    def footprint(
            self,
            half_side: np.int32 = None,
            location_name: str = None,
            terminal_file_path:str  = None)-> None:
        """Getting the foot print
        
        Args:
            half_side: Lenght of the half side of AOI in Km.
            location_name: Name of the location from xlsx file
            terminal_file_path: Path to the oil terminal data file
        """
        if not os.path.exists(terminal_file_path):
            self.foot_print = None
            self.log.error(f"{terminal_file_path} is not filepath or does not exist")
        else:
            # Getting the coordinates of the location
            terminal_dict = oil_terminals(
                terminal_file_path = terminal_file_path)
            for loc_name, coords in terminal_dict.items():
                if location_name == loc_name:
                    self.center_coords_lat = coords[0]
                    self.center_coords_lon = coords[1]

                    # Getting the footprint polygon
                    self.foot_print = bbox(
                        half_side = half_side,
                        center_lat = self.center_coords_lat,
                        center_lon = self.center_coords_lon
                        )
                    break                   
                else:
                    self.foot_print = None
                    self.log.error(f"{location_name} is not in {terminal_file_path}")
        
        return self.foot_print
    
    def query(
            self,
            start_date:str = None,
            end_date:str = None,
            platformname:str = 'Sentinel-1',
            producttype:str = 'GRD'):
        """Fucntion to query scihub
        
        Args:
            start_date: Start date of the search. eg: 2023-02-01
            end_date: End date of the search, eg: 2023-03-21
            platformname: Name of the platform, Sentinel-1
            producttype: Type of the sentinel-1 data product, eg: 'SLC', 'GRD' 
        """
        # Getting the dates
        startdate = start_date.split('-')
        startdate = stitch_strings(startdate)
        enddate = end_date.split('-')
        enddate = stitch_strings(enddate)

        # Getting the polygon object
        self.aoi = loads(self.foot_print)

        # Getting the products
        self.products = self.api.query(self.aoi,
                     date=(startdate, enddate),
                     platformname=platformname,
                     producttype=producttype)
        return self.api.to_dataframe(self.products) # Returning a dataframe of the results

    def swath_aoi_check(self)-> None:
        """This function helps to filter swaths which has our AOI"""
        # Checking if the AOI falls within the downloadble swaths
        self.products_df = self.api.to_dataframe(self.products)
        swath_polygons = self.products_df['footprint'].values

        for i in range(len(swath_polygons)):
            multi_polygon = loads(swath_polygons[i])
            if self.aoi.within(multi_polygon):
                self.log.info("Desired swath has been identified!")
                self.uuid = self.products_df['uuid'][i]
                self.title = self.products_df['title'][i]
                break
            else:
                self.log.debug("No desired swath has been indentified!")
                self.log.debug("Expand the search parameters such as datetimes")
                self.log.debug("and mkae sure the foot print is on the land")
                self.uuid = None
        
        return self.title, self.uuid 
        # Returns the title S1A_IW__XXX_XXXXXX
        # Returns uuid 3ae4b23xxxxxxxxxxxxxxxx