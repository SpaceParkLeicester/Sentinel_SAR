import json
import os
import random
import sys
import numpy as np

from oil_storage_tanks.utils import logger
from oil_storage_tanks.data.scihub import SearchSciHubData, DownloadSciHubData

# Retrieve Job-defined env vars
TASK_INDEX = os.getenv("CLOUD_RUN_TASK_INDEX", 0)
TASK_ATTEMPT = os.getenv("CLOUD_RUN_TASK_ATTEMPT", 0)
# Retrieve User-defined env vars
SLEEP_MS = os.getenv("SLEEP_MS", 0)
FAIL_RATE = os.getenv("FAIL_RATE", 0)

class sar_preprocess:
    """Cloud Run SAR pre-process"""
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
            half_side:np.int64 = None,
            location_name:str = None,
            start_date:str = None,
            end_date:str = None)-> None:
        """Search data from scihub"""
        self.scihub = SearchSciHubData(
            log = self.log,
            data_service = self.data_service,
            path_to_cred_file = self.path_to_cred_file)
        self.foot_print = self.scihub.footprint(
            half_side = half_side,
            location_name = location_name)
        self.api_df = self.scihub.query(
            start_date = start_date,
            end_date = end_date)
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
            download_scihub.download_sensat(
                uuid = self.uuid,
                title = self.title,
                download_path = download_path)
        else:
            self.log.debug("search credentials did not provide a desirable results")
            self.log.debug("Try with different parameters")

# Throw an error based on fail rate
def random_failure(rate):
    if rate < 0 or rate > 1:
        # Return without retrying the Job Task
        print(
            f"Invalid FAIL_RATE env var value: {rate}. " +
            "Must be a float between 0 and 1 inclusive."
        )
        return

    random_failure = random.random()
    if random_failure < rate:
        raise Exception("Task failed.")


if __name__ == "__main__":
    data_service = 'Copernicus scihub account'
    path_to_cred_file = '.privatae/cred.json'
    download_path = '/mnt/disks/diss_dir/SAFE'
    half_side = 10
    location_name = 'Stanlow'
    start_date = '2023-03-01'
    end_date = '2023-03-04'

    try:
        sar = sar_preprocess(
            data_service = data_service,
            path_to_cred_file = path_to_cred_file,
            log = logger())
        sar.search_data(
            half_side = half_side,
            location_name = location_name,
            start_date = start_date,
            end_date = end_date)
        sar.download_data(download_path = download_path)

        # Errors
        random_failure(float(FAIL_RATE))

    except Exception as err:
        message = f"Task #{TASK_INDEX}, " \
                  + f"Attempt #{TASK_ATTEMPT} failed: {str(err)}"

        print(json.dumps({"message": message, "severity": "ERROR"}))
        sys.exit(1)  # Retry Job Task by exiting the process
