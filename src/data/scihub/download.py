"""Downloading data from Copernicus Data Hub"""
import os
from src.data import AuthCredentials
from src.data.scihub import SearchSciHubData

import logging
from logging import config
config.fileConfig('logger.ini')
logger = logging.getLogger(__name__)


class DownloadSciHubData(AuthCredentials):
    """Function to download single scene"""
    def __init__(self, log: isinstance = None) -> None:
        """Inheriting and declaring variables
        
        Args:
            data_service: Name of the data service, eg: "Copernicus"
            log: Custom logger function
        """
        super().__init__(log)        
        self.api = super().scihub_auth()
    
    def download_sensat(
            self,
            uuid:str = None,
            title:str = None,
            download_path: str = None)-> None:
        """Downloading a single product
        
        Args:
            title: title of the file
            uuid: Identifier of the a file
            download_path: Download path folder
        """
        # Downloading the data
        zip_file = title + '.zip'
        zip_filepath = os.path.join(download_path, zip_file)
        if not os.path.exists(zip_filepath):
            self.log.info(f"Commencing {title} download")
            self.api.download(uuid, download_path)
        else:
            self.log.debug("File already exists!")
        return zip_filepath

if __name__ == "__main__":
    download_path = 'downloads/S1_data/'
    download_path = os.path.join(os.path.expanduser('~'), download_path)

    search = SearchSciHubData(log = logger)
    search.footprint(location_name = 'stanlow')
    search.query()
    title, uuid = search.swath_aoi_check()

    download = DownloadSciHubData(log = logger)
    download.download_sensat(
        uuid = uuid,
        title = title,
        download_path = download_path)
