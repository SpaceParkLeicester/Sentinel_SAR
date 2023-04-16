import os
from oil_storage_tanks.utils import logger
from oil_storage_tanks.data.scihub import (
    SearchSciHubData, 
    DownloadSciHubData)

class download_sar:
    """Jobs- Run SAR pre-process"""
    def __init__(
            self,
            data_service:str = None, 
            path_to_cred_file:str = None,
            download_path:str = None,
            location_name:str = None,                    
            log: isinstance = None) -> None:
        """Definig variables
        
        Args:
            data_service: Name of the data service
        """
        self.log = log
        self.data_service = data_service
        self.path_to_cred_file = path_to_cred_file
        self.download_path = download_path
        self.location_name = location_name
  
    def search_data(self)-> None:
        """Search data from scihub"""
        # Querying with scihub API
        self.scihub = SearchSciHubData(
            log = self.log,
            data_service = self.data_service,
            path_to_cred_file = self.path_to_cred_file)
        self.foot_print = self.scihub.footprint(location_name = self.location_name)
        self.api_df = self.scihub.query()
        self.title, self.uuid = self.scihub.swath_aoi_check()
    
    def download_data(self)-> None:
        """Download data from scihub"""
        # Downloading the data
        download_path = os.path.join(self.download_path, self.location_name)
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        if self.title is not None:
            download_scihub = DownloadSciHubData(
                log = self.log,
                data_service = self.data_service,
                path_to_cred_file = self.path_to_cred_file)
            self.zip_filepath = download_scihub.download_sensat(
                uuid = self.uuid,
                title = self.title,
                download_path = download_path)
            return self.zip_filepath
        else:
            self.log.debug("search credentials did not provide a desirable results")
            self.log.debug("Try with different parameters")
            return None

if __name__ == "__main__":
    data_service = 'Copernicus scihub account'
    path_to_cred_file = '.private/cred.json'
    download_path = '/mnt/disks/diss_dir/SAFE'
    location_name = 'stanlow'

    sar = download_sar(
        data_service = data_service,
        path_to_cred_file = path_to_cred_file,
        download_path = download_path,
        location_name = location_name,                
        log = logger())
    sar.search_data()
    sar.download_data()
