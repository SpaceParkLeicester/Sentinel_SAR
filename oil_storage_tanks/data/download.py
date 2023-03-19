import os
import json
import logging
import asf_search as asf
from datetime import datetime
from typing import Optional
import numpy as np
from oil_storage_tanks.data import bounding_box as bbox

def logger():
    # Configure logging to display on console
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

    # Add a console handler
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger(__name__).addHandler(console)
    return logging    

class s1_data_download():
    """Download the Sentinel1 data"""
    def __init__(
            self,
            wkt_aoi: Optional[str] = None,            
            start_date:str = "2023-03-10",
            end_date:str = "2023-03-18"
            ) -> None:       
        """Declaring the variables
            start_date: Start date of the search
            end_date: End date of the search
            wkt_aoi: Bounding box of the polygon     
        """
        self.start_date = start_date
        self.end_date = end_date
        self.wkt_aoi = wkt_aoi
        self.log = logger()

    def earthdata_auth(
            self,
            earthdata_cred: str = ".private/earthdata_cred.json"
            ) -> None:
        """Authentication of Earthdata
        
        Args:
            earthdata_cred: Path to earthdata credentials
        """
        # Reading earth data credentials from json file
        if os.path.exists(earthdata_cred):
            self.log.info("Getting info from the credential file")
            with open(earthdata_cred) as f:
                earthdata = json.load(f)
                username = earthdata['username']
                password = earthdata['password']
            # Calling the ASF EARTHDATA API
            self.log.info("Starting the ASF session auth with")
            self.log.info(f"username:{username} and password:{password}")
            self.session = asf.ASFSession().auth_with_creds(username, password)
            f.close()
            if self.session is not None:
                self.log.info("Authentication successful!")
        else:
            self.log.debug("Please add crednetial JSON file")
    
    def s1_metadata(
            self,
            center_coords_lat: np.float64 = 58.83834793,
            center_coords_lon: np.float64 = -3.121350468
            ):
        """Getting the meta data of the scene
        
        Args:
            center_coords_lat: Center Latitude of AOI
            center_coords_lon: Center Longitude of AOI         
        """
        # Getting the WKT from center coordinates
        self.log.info(f"Looking data for the coords:{center_coords_lat},{center_coords_lon}")
        if self.wkt_aoi is None:
            self.wkt_aoi = bbox(
                center_lat = center_coords_lat,
                center_lon = center_coords_lon)
        else:
            self.log.info(f"WKT of AOI is {self.wkt_aoi}")

        # Date objects
        self.log.info(f"Searching data for the dates between {self.start_date}:{self.end_date}")
        start = datetime.strptime(self.start_date, "%Y-%m-%d")
        end = datetime.strptime(self.end_date, "%Y-%m-%d")

        # Getting the results of the search
        self.results = asf.search(
            platform= asf.PLATFORM.SENTINEL1A,
            processingLevel=[asf.PRODUCT_TYPE.SLC],
            start = start,
            end = end,
            intersectsWith = self.wkt_aoi
            )  
        self.log.info(f'Total Images Found: {len(self.results)}')
        self.log.info(f'The metadata for the results are:\n{self.results}')

        ### Save Metadata to a Dictionary
        metadata = self.results.geojson()

        # Sanity check
        assert metadata is not None
        
        return metadata
    
    def download_data(
            self,
            download_path: str = "data/") -> None:
        """
        Downloads the data
        
        Args:
            download_path: Set the download path
            path_to_cred_file: Path to the credential file
        """
        # Start the download
        self.log.info(f"The download path is {download_path}")
        self.results.download(
            path = download_path,
            session = self.session, 
            processes = 2
            )

if __name__ == "__main__":
    earthdata = s1_data_download()
    earthdata.s1_metadata()
