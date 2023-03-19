import os
import logging
import json
import asf_search as asf
from datetime import datetime
from typing import Optional
import numpy as np
import argparse
from oil_storage_tanks.data import bounding_box as bbox

# Custom logger function
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class s1_data_download():
    """Download the Sentinel1 data"""
    def __init__(
            self,
            center_coords_lat: np.float64 = None,
            center_coords_lon: np.float64 = None,
            wkt_aoi: Optional[str] = None,            
            start_date:str = "2023-01-01",
            end_date:str = "2023-03-17"
            ) -> None:       
        """Declaring the variables
            start_date: Start date of the search
            end_date: End date of the search
            wkt_aoi: Bounding box of the polygon
            center_coords_lat: Center Latitude of AOI
            center_coords_lon: Center Longitude of AOI      
        """
        self.start_date = start_date
        self.end_date = end_date
        self.wkt_aoi = wkt_aoi
        self.center_coords_lat = center_coords_lat
        self.center_coords_lon =center_coords_lon

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
            with open(earthdata_cred) as f:
                earthdata = json.load(f)
                username = earthdata['username']
                password = earthdata['password']
            # Calling the ASF EARTHDATA API
            self.session = asf.ASFSession().auth_with_creds(username, password)
            f.close()
        else:
            log.debug("Please add crednetial JSON file")

    def s1_metadata(self):
        """Getting the meta data of the scene"""
        # Getting the WKT from center coordinates
        if self.wkt_aoi is None:
            self.wkt_aoi = bbox(
                center_lat = self.center_coords_lat,
                center_lon = self.center_coords_lon)
        
        # Date objects
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
            download_path: str = "data") -> None:
        """
        Downloads the data
        
        Args:
            download_path: Set the download path
            path_to_cred_file: Path to the credential file
        """
        # Start the download
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
    earthdata = s1_data_download(
        center_coords_lat = args.center_lat,
        center_coords_lon = args.center_lon
    )
    metadata = earthdata.s1_metadata()