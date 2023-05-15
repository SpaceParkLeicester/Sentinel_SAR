import os
from pathlib import Path
from oil_storage_tanks.utils import unzip_s1data
from oil_storage_tanks.google_bucket import GoogleBuckets
from oil_storage_tanks.utils import logger
from oil_storage_tanks.data.scihub import (
    SearchSciHubData, 
    DownloadSciHubData)

class download_sar:
    """Jobs- Run SAR pre-process"""
    def __init__(
            self,
            path_to_cred_file:str = None,
            download_path:str = None,
            location_name:str = None,                    
            log: isinstance = None) -> None:
        """Definig variables
        
        Args:
            data_service: Name of the data service
        """
        self.log = log
        self.path_to_cred_file = path_to_cred_file
        self.download_path = download_path
        self.location_name = location_name
  
    def search_data(self)-> None:
        """Search data from scihub"""
        # Querying with scihub API
        self.scihub = SearchSciHubData(
            log = self.log,
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
            self.log.info(f"Downloading data of Oil termianl at {self.location_name}")
            download_scihub = DownloadSciHubData(
                log = self.log,
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
        
    def unzipping_s1data(self)-> None:
        """Unzip the S1 data"""
        self.download_path = Path(self.zip_filepath).parent.absolute()
        self.unzip_dir_filename = Path(self.zip_filepath).stem
        self.safe_folder_path = unzip_s1data(
            download_path = self.download_path,
            path_to_zip_file = self.zip_filepath,
            unzip_dir_filename = self.unzip_dir_filename,
            log = self.log)        
    
    def upload_gcp_bucket(
            self,
            bucket_path:str = None)-> None:
        """upload to the GCP bucket"""
        # Initiating the Google Bucket upload function
        data_upload = GoogleBuckets(
            local_filepath = self.safe_folder_path,
            bucket_path = bucket_path,
            log = self.log)
        # Uploading the file
        data_upload.upload()
        # Removing uploaded files locally
        data_upload.remove_uploaded_files()


if __name__ == "__main__":
    path_to_cred_file = '.private/cred.json'
    download_path = '/mnt/disks/diss_dir/SAFE'
    location_name = 'shetland'

    sar = download_sar(
        path_to_cred_file = path_to_cred_file,
        download_path = download_path,
        location_name = location_name,                
        log = logger())
    sar.search_data()
    sar.download_data()
