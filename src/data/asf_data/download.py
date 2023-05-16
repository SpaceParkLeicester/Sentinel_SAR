"""Function to download the ASF data"""
import os
from urllib.parse import urlparse
import time 
import asf_search as asf
from src.data import AuthCredentials

import logging
from logging import config
config.fileConfig('logger.ini')
logger = logging.getLogger(__name__)
    

class DownloadASFData(AuthCredentials):
    """Functions relating to download data from ASF"""
    def __init__(self, log: isinstance = None) -> None:
        super().__init__(log = log)
        self.api = super().earthdata_auth()
        self.log = log
    
    def download_data(
            self,
            download_path: str = None,
            asf_data_url:str = None)-> None:
        """Commencing the download"""
        # Getting the UUID from the url
        self.url_path = urlparse(asf_data_url)
        self.uuid_zip = os.path.basename(self.url_path.path)

        # Checking if the file exists
        self.filepath = os.path.join(download_path, self.uuid_zip)
        if not os.path.exists(self.filepath):
            logger.info(f"Commencing download of the file {self.uuid_zip}")
            # Starting the download session
            asf.download_url(
                url = asf_data_url,
                path = download_path,
                filename = self.uuid_zip,
                session = self.user_pass_session)
            time.sleep(5)
            self.log.info("Download is finished!")
        else:
            self.log.debug(f"File {self.uuid_zip} already exists!")

if __name__ == "__main__":
    asf_data_url = 'https://datapool.asf.alaska.edu/SLC/SA/S1A_IW_SLC__1SDV_20230112T175210_20230112T175237_046754_059AE5_4A45.zip'
    download_path = '/home/vardh/apps/tmp'
    download = DownloadASFData(log = logger)
    download.download_data(download_path,asf_data_url)
    
