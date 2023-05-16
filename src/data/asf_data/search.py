"""Functions relating to search"""
import os
import numpy as np
from datetime import datetime

import asf_search as asf
from src.utils import stitch_strings
from src.data import OilTerminals


class SearchEarthData:
    """Refine Search results from ASF EARTH DATA"""
    def __init__(
            self,
            start_date:str = "2023-03-10",
            end_date:str = "2023-03-18",
            location_name:str = "flotta",                      
            log=None) -> None:
        """Getting the meta data of the scene
        
        Args:
            start_date: Start date of the search
            end_date: End date of the search
            location_name: Location name of the oil terminal
            log: Custom logger function        
        """       
        self.start_date = start_date
        self.end_date = end_date
        self.location_name = location_name
        self.log = log

    def metadata(
            self,
            platform_name:str = 'SENTINEL1A', # SENTINEL1A or SENTINEL1B,
            product_type:str = 'GRD', # SLC or GRD
            half_side: np.int64 = None):
        """Getting the meta data as per search details
        
        Args:
            platform_name: Name of the Sentinel platform.
            product_type: Type of the product.
            half_side: Half side of AOI.
        """
        # Getting the WKT from center coordinates
        self.log.info(f"Getting metadata for {self.location_name}")
        self.log.info(f"from {self.start_date} to {self.end_date}")
        # Initiating Oil Terminals function
        self.oilterminals = OilTerminals()
        self.data = self.oilterminals.read_data()
        self.wkt_aoi = self.oilterminals.bounding_box(
            center_lat = self.data[self.location_name][0],
            center_lon = self.data[self.location_name][1],
            half_side = half_side)

        # Date objects
        self.start = datetime.strptime(self.start_date, "%Y-%m-%d")
        self.end = datetime.strptime(self.end_date, "%Y-%m-%d")

        # Getting the results of the search
        self.results = asf.search(
            platform = asf.PLATFORM.SENTINEL1A,
            processingLevel = [asf.PRODUCT_TYPE.GRD_HD],
            start = self.start,
            end = self.end,
            intersectsWith = self.wkt_aoi
            )
        
        # Sanity check
        try:
            total_results = len(self.results)
            assert total_results > 0
            self.log.info(f'Total Images Found: {len(self.results)}')
            ### Save Metadata to a Dictionary
            self.metadata = self.results.geojson()
            return self.metadata 
                   
        except AssertionError:    
            self.log.debug("No images are found for the given criteria!")
            return None
    
    def save_search(
            self,
            csv_file_save_path: str):
        """Function to save the search results"""
        # Defining the filename and the path
        start_date = self.start_date.replace('-', '')
        end_date = self.end_date.replace('-', '')
        filename = ["s1", self.location_name, start_date, end_date]
        filename = stitch_strings(filename, "_")
        self.csv_folder_path = os.path.join(csv_file_save_path, self.location_name)
        self.csv_filepath = os.path.join(self.csv_folder_path, filename + ".csv")

        # Writing the file
        if not os.path.exists(self.csv_folder_path):
            self.log.info(f"Creating the folder {self.location_name}")
            os.makedirs(self.csv_folder_path)
        else:
            self.log.debug(f"The folder '{self.location_name}' exists!")

        if not os.path.isfile(self.csv_filepath):
            with open(self.csv_filepath, "w") as f:
                f.writelines(self.results.csv())
                f.close()
                self.log.info(f"The file is saved to: {self.csv_filepath}")
        else:
            self.log.debug(f"The file already exists: {self.csv_filepath}")
        
        return self.csv_filepath
