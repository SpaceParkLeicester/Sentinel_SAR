import os
import logging
import json
import asf_search as asf
from datetime import datetime
from typing import Optional
import numpy as np
import argparse
from oil_storage_tanks.data import bounding_box as bbox

log = logging.getLogger(__name__)

class s1_data_download():
    """Download the Sentinel1 data"""
    def __init__(
            self,
            wkt_aoi: Optional[str] = None,            
            start_date:str = "2023-01-01",
            end_date:str = "2023-03-17"
            ) -> None:       
        """Declaring the variables
            start_date: Start date of the search
            end_date: End date of the search
            wkt_aoi: Bounding box of the polygon     
        """
        self.start_date = start_date
        self.end_date = end_date
        self.wkt_aoi = wkt_aoi

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
            log.info("Getting info from the credential file")
            with open(earthdata_cred) as f:
                earthdata = json.load(f)
                username = earthdata['username']
                password = earthdata['password']
            # Calling the ASF EARTHDATA API
            log.info("Starting the ASF session auth with")
            log.info(f"username:{username} and password:{password}")
            self.session = asf.ASFSession().auth_with_creds(username, password)
            f.close()
            if self.session is not None:
                log.info("Authentication successful!")
        else:
            log.debug("Please add crednetial JSON file")

    def s1_metadata(
            self,
            center_coords_lat: np.float64 = None,
            center_coords_lon: np.float64 = None
            ):
        """Getting the meta data of the scene
        
        Args:
            center_coords_lat: Center Latitude of AOI
            center_coords_lon: Center Longitude of AOI         
        """
        # Getting the WKT from center coordinates
        log.info(f"WKT of AOI is {self.wkt_aoi}")
        log.info(f"Looking data for the coords:{center_coords_lat},{center_coords_lon}")
        if self.wkt_aoi is None:
            self.wkt_aoi = bbox(
                center_lat = center_coords_lat,
                center_lon = center_coords_lon)
        
        # Date objects
        log.info(f"Searching data for the dates between {self.start_date}:{self.end_date}")
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
        log.info(f'Total Images Found: {len(self.results)}')

        ### Save Metadata to a Dictionary
        metadata = self.results.geojson()
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
        log.info(f"The download path is {download_path}")
        self.results.download(
            path = download_path,
            session = self.session, 
            processes = 2
            )

if __name__ == "__main__":
    # Adding parser for the user input
    parser = argparse.ArgumentParser(description = 'Earth data ASF browsing and downloading')
    parser.add_argument(
        'center_lat',
        metavar = 'CENTER_LATITUDE',
        type = np.float64,
        help = 'Enter the Center Latitude of the AOI')
    parser.add_argument(
        'center_lon',
        metavar = 'CENTER_LONGITUDE',
        type = np.float64,
        help = "Enter the center longitude of the AOI"
    )
    parser.add_argument(
        '--log-level', 
        dest='log_level', 
        default='INFO', 
        help='Set the logging level')
    args = parser.parse_args()

    # Set the logging level
    log.setLevel(getattr(logging, args.log_level.upper()))    

    log.info("Initiating the EarthData seach with ASF")
    earthdata = s1_data_download()
    metadata = earthdata.s1_metadata(
        center_coords_lat = args.center_lat,
        center_coords_lon = args.center_lon        
    )