"""Downloading data for the SAR pre-processing"""
import json
import numpy as np
from oil_storage_tanks.utils import logger
from shapely.geometry import Polygon, MultiPolygon
from shapely.wkt import loads
from oil_storage_tanks.utils import bounding_box as bbox
from oil_storage_tanks.data.asf_data import earthdata_auth, download_asf
from sentinelsat import SentinelAPI

class download_data(earthdata_auth):
    """Function to download single scene"""
    def __init__(
            self, 
            path_to_cred_file: str = None, 
            log=None) -> None:
        """Inherting from the auth function
        
        Args:
            path_to_cred_file: Path to the credentail file
            log: Custom logger function
        """
        super().__init__(path_to_cred_file, log)
        self.log = log
        self.user_pass_session = super().auth()
    
    def sensat_api_query(
            self,
            center_lat_coords:np.float64 = None,
            center_lon_coords: np.float64 = None,
            half_side: np.int32 = None)-> None:
        """Authenticating scihub account
        
        Args:
            center_lat_coords: Center Latitude
            center_lon_coords: Center Longitude
            half_side: Half side of the bbox
        """
        # Reading the credential file
        with open(self.path_to_cred_file) as f:
            cred_file = json.load(f)
            user = cred_file['user']
            password = cred_file['password']
            f.close()
        
        # Initiate Sentinel API
        self.api = SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus')

        # Getting the WKT
        self.footprint = bbox(
            half_side = half_side,
            center_lat = center_lat_coords,
            center_lon = center_lon_coords) 
        # WKT string to shapely object
        self.aoi = loads(self.footprint)
        # Getting the products
        self.products = self.api.query(self.footprint,
                     date=('20230101', '20230402'),
                     platformname='Sentinel-1',
                     producttype='SLC')
        self.log.info('Following products are available')
        self.log.info(self.api.to_dataframe(self.products).title.values)
    
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
                break
            else:
                self.uuid = None
    
    def download_sensat(
            self,
            identifier:str = None,
            download_path: str = None)-> None:
        """Downloading a single product
        
        Args:
            identifier: Identifier of the a file
            download_path: Download path folder
        """
        if identifier is not None:
            # Filter the UUID from an Identifier
            uuid_df = self.products_df[self.products_df['title'] == identifier]
            uuid = uuid_df['uuid'].values        
            self.api.download(
                uuid[0],
                download_path)
        else:
            if self.uuid is not None:
                # Downloading a single scene
                self.api.download(
                    self.uuid, 
                    directory_path = download_path)
            else:
                self.log.debug("No product has been found for the desired AOI polygon!")
                self.log.debug("Expand the search requirements such as dates, or other coordinates for AOI")

    
    def commence_download(
            self,
            download_path:str = None,
            csv_search_results_path:str = None)-> None:
        """Downloading one scene from the seacth results"""
        # Calling Download function
        data_download = download_asf(
            user_pass_session = self.user_pass_session,
            download_path = download_path,
            csv_search_results_path = csv_search_results_path,
            log = self.log
        )
        data_download.check_files()
        data_path = data_download.get_download_path()
        data_download.download_data()
        return data_path
        
if __name__ == "__main__":
    path_to_cred_file = '.private/earthdata_cred.json'
    download_path = 'data/SAFE'
    csv_seach_results_path = 'data/s1_data_search_results/Flotta/s1_Flotta_20230101_20230115.csv'
    identifier = 'S1A_IW_SLC__1SDV_20230327T062256_20230327T062324_047826_05BF02_063C'
    dl = download_data(
        path_to_cred_file = path_to_cred_file,
        log = logger())
    dl.sensat_api_query(
        half_side = 10,
        center_lat_coords = 53.6442984,
        center_lon_coords = -0.254176842)
    dl.swath_aoi_check()
    dl.download_sensat(
        identifier = identifier,
        download_path = download_path)
