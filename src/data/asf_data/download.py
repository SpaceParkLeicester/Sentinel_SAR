"""Function to download the ASF data"""
import os
from urllib.parse import urlparse
import time 
import asf_search as asf
    

class DownloadASFData():
    """Functions relating to download data from ASF"""
    def __init__(
            self, 
            user_pass_session: asf.ASFSession = None,
            download_path: str = None,
            asf_data_url:str = None,      
            log = None) -> None:
        """ Initialising the logger"""        
        self.log = log
        self.asf_data_url = asf_data_url
        self.user_pass_session = user_pass_session
        self.download_path = download_path
    
    def download_data(self)-> None:
        """Commencing the download"""
        # Getting the UUID from the url
        self.url_path = urlparse(self.asf_data_url)
        self.uuid_zip = os.path.basename(self.url_path.path)

        # Checking if the file exists
        self.filepath = os.path.join(self.download_path, self.uuid_zip)
        if not os.path.exists(self.filepath):
            self.log.info(f"Commencing download of the file {self.uuid_zip}")
            # Starting the download session
            asf.download_url(
                url = self.asf_data_url,
                path = self.download_path,
                filename = self.uuid_zip,
                session = self.user_pass_session)
            time.sleep(5)
            self.log.info("Download is finished!")
        else:
            self.log.debug(f"File {self.uuid_zip} already exists!")
