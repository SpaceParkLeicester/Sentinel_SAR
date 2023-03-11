from utils import earthdata_authentication as auth
from utils import bounding_box as bbox

import asf_search as asf
import geopandas as gpd
from shapely.geometry import box
from datetime import datetime
import logging

log = logging.getLogger(__name__)

class s1_data():
    """Download the Sentinel1 data"""
    def __init__(
            self,
            start_date:str,
            end_date:str,
            wkt_aoi: str) -> None:
        """Declaring the variables
            start_date = Start date of the search
            end_date = End date of the search
            wkt_aoi = Bounding box of the polygon        
        """
        self.start_date = start_date
        self.end_date = end_date
        self.wkt_aoi = wkt_aoi

    def s1_metadata(self) -> None:
        """Getting the meta data of the scene"""
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
        log.info(f"The results of the search were {metadata}")
    
    def download_data(
            self,
            path_to_download: str,
            path_to_cred_file:str) -> None:
        """Downloads the data"""
        # Authenticate the login details
        session = auth(cred_file_path = path_to_cred_file)

        # Start the download
        self.results.download(
            path = path_to_download,
            session = session, 
            processes = 2
            )