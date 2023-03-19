"""Functions relating to search"""
import os
import numpy as np
import asf_search as asf
from datetime import datetime
from typing import Dict
from oil_storage_tanks.utils import logger, stitch_strings
from oil_storage_tanks.data import bounding_box as bbox

class asf_search():
    """Refine Search results from ASF EARTH DATA"""
    def __init__(
            self,
            start_date:str = "2023-03-10",
            end_date:str = "2023-03-18",            
            center_coords_lat: np.float64 = 58.83834793,
            center_coords_lon: np.float64 = -3.121350468) -> None:
        """Getting the meta data of the scene
        
        Args:
            start_date: Start date of the search
            end_date: End date of the search
            center_coords_lat: Center Latitude of AOI
            center_coords_lon: Center Longitude of AOI         
        """
        self.start_date = start_date
        self.end_date = end_date
        self.center_coords_lat = center_coords_lat
        self.center_coords_lon = center_coords_lon
        self.log = logger()
    
    def metadata(self) -> Dict:
        # Getting the WKT from center coordinates
        self.log.info(f"Looking data for the coords:{self.center_coords_lat},{self.center_coords_lon}")
        self.wkt_aoi = bbox(
            center_lat = self.center_coords_lat,
            center_lon = self.center_coords_lon)

        # Date objects
        self.log.info(f"Searching data for the dates between {self.start_date}:{self.end_date}")
        self.start = datetime.strptime(self.start_date, "%Y-%m-%d")
        self.end = datetime.strptime(self.end_date, "%Y-%m-%d")

        # Getting the results of the search
        self.results = asf.search(
            platform= asf.PLATFORM.SENTINEL1A,
            processingLevel=[asf.PRODUCT_TYPE.SLC],
            start = self.start,
            end = self.end,
            intersectsWith = self.wkt_aoi
            )  
        self.log.info(f'Total Images Found: {len(self.results)}')

        ### Save Metadata to a Dictionary
        self.metadata = self.results.geojson()

        # Sanity check
        assert self.metadata is not None
        
        return self.metadata
    
    def save_search(
            self,
            file_save_path: str):
        """Fucntion to save the search results"""
        # Definig the filename and the path
        start_date = self.start_date.replace('-', '')
        end_date = self.end_date.replace('-', '')
        filename = ["s1", start_date, end_date]
        filename = stitch_strings(filename, "_")
        filepath = os.path.join(file_save_path,filename + ".csv")

        # Writing the file
        if not os.path.exists(filepath):
            with open(filepath, "w") as f:
                f.writelines(self.results.csv())
                f.close()
                self.log.info(f"The file is saved to: {filepath}")
        else:
            self.log.debug(f"The file already exists: {filepath}")


if __name__ == "__main__":
    # Calling above functions
    file_save_path = "data/s1_data"
    asf_earthdata = asf_search()
    asf_earthdata.metadata()
    asf_earthdata.save_search(
        file_save_path = file_save_path
    )