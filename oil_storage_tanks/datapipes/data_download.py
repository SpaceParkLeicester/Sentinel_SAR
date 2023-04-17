import os
from oil_storage_tanks.utils import logger
from oil_storage_tanks.data import OilTerminals
from oil_storage_tanks.jobs.sar_data import download_sar

class sar_download_datapipe:
    """SAR data download datapipe"""
    def __init__(
            self,
            path_to_cred_file:str = None,
            download_path:str = None,
            bucket_path:str = None,
            log:isinstance = None) -> None:
        """Datapipe to download data for every Oil Terminal location
        
        Args:
            path_to_cred_file: Path to the crednetial file
            download_path: S1 data download path
            bucket_name: uploading to this GCP bucket path
            log: Custom logger function
        """
        self.path_to_cred_file = path_to_cred_file
        self.download_path = download_path
        self.bucket_path = bucket_path
        self.log = log
    
    def download_data(self)-> None:
        """Downloading and uploading data to GCP"""
        oiltermianls = OilTerminals()
        data_dict = oiltermianls.read_data()
        for location_name, _ in data_dict.items():
            bucket_path = os.path.join(self.bucket_path, location_name)
            sar = download_sar(
                path_to_cred_file = self.path_to_cred_file,
                download_path = self.download_path,
                location_name = location_name,
                log = self.log)
            sar.search_data()
            sar.download_data()
            sar.unzipping_s1data()
            sar.upload_gcp_bucket(
                bucket_path = bucket_path)

if __name__ == "__main__":
    path_to_cred_file = '.private/cred.json'
    download_path = '/mnt/disks/diss_dir/SAFE'
    bucket_path = 's1-data/SAFE'
    sar_data = sar_download_datapipe(
        path_to_cred_file = path_to_cred_file,
        download_path = download_path,
        bucket_path = bucket_path,
        log = logger())
    sar_data.download_data()
        
