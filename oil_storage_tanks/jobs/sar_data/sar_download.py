import numpy as np
from oil_storage_tanks.utils import logger
from oil_storage_tanks.data.scihub import SearchSciHubData, DownloadSciHubData
from oil_storage_tanks.batch_preprocessing import esa_snap_graph

class download_sar:
    """Jobs- Run SAR pre-process"""
    def __init__(
            self,
            data_service:str = None, 
            path_to_cred_file:str = None,
            log: isinstance = None) -> None:
        """Definig variables"""
        self.log = log
        self.data_service = data_service
        self.path_to_cred_file = path_to_cred_file
  
    def search_data(
            self,
            location_name:str = None)-> None:
        """Search data from scihub"""
        self.scihub = SearchSciHubData(
            log = self.log,
            data_service = self.data_service,
            path_to_cred_file = self.path_to_cred_file)
        self.foot_print = self.scihub.footprint(location_name = location_name)
        self.api_df = self.scihub.query()
        self.title, self.uuid = self.scihub.swath_aoi_check()
    
    def download_data(
            self,
            download_path:str = None)-> None:
        """Download data from scihub"""
        if self.title is not None:
            download_scihub = DownloadSciHubData(
                log = self.log,
                data_service = self.data_service,
                path_to_cred_file = self.path_to_cred_file)
            filepath = download_scihub.download_sensat(
                uuid = self.uuid,
                title = self.title,
                download_path = download_path)
            return filepath
        else:
            self.log.debug("search credentials did not provide a desirable results")
            self.log.debug("Try with different parameters")
            return None
        


if __name__ == "__main__":
    data_service = 'Copernicus scihub account'
    path_to_cred_file = '.private/cred.json'
    download_path = '/mnt/disks/diss_dir/SAFE'
    half_side = 10
    location_name = 'stanlow'
    start_date = '2023-03-01'
    end_date = '2023-03-04'

    sar = download_sar(
        data_service = data_service,
        path_to_cred_file = path_to_cred_file,
        log = logger())
    sar.search_data(
        half_side = half_side,
        location_name = location_name,
        start_date = start_date,
        end_date = end_date)
    sar.download_data(download_path = download_path)
