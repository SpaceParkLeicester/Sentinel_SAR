"""Downloading data from Copernicus Data Hub"""
import os
from src.data import AuthCredentials

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
    
