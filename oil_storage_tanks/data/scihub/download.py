"""Downloading data from Copernicus Data Hub"""
import os
from oil_storage_tanks.utils import unzip_scihub_s1data
from oil_storage_tanks.utils import logger
from oil_storage_tanks.data.scihub import search_data
from oil_storage_tanks.data import auth_credentials

class download_data(auth_credentials):
    """Function to download single scene"""
    def __init__(
            self, 
            data_service: str = None, 
            path_to_cred_file: str = None,
            username:str = None,
            password:str = None,            
            log=None) -> None:
        super().__init__(
            data_service, path_to_cred_file,
            username, password, log)
        super().credentials()
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
        zip_file = title + '.SAFE'
        zip_filepath = os.path.join(download_path, zip_file)
        if not os.path.exists(zip_filepath):
            self.log.info(f"Commencing {title} download")
            self.api.download(uuid, download_path)
        else:
            self.log.debug("File already exists!")
        
        # Extracting the zip data
        # zip_extract = unzip_scihub_s1data(
        #     download_path = download_path,
        #     path_to_zip_file = zip_filepath,
        #     unzip_dir_filename = title,
        #     log = log)


if __name__ == '__main__':
    path_to_cred_file = '.private/cred.json'
    terminal_file_path = 'data/uk_oil_terminals.xlsx'
    data_service = 'Copernicus scihub'
    download_path = '/mnt/disks/diss_dir/SAFE'
    half_side = 10
    location_name = 'flotta'
    start_date = '2023-03-01'
    end_date = '2023-03-05'
    log = logger()
    search = search_data(
        data_service = data_service,
        path_to_cred_file = path_to_cred_file,
        log = log)
    search.footprint(
        half_side = half_side,
        location_name = location_name,
        terminal_file_path = terminal_file_path)
    search.query(
        start_date = start_date,
        end_date = end_date)
    title, uuid = search.swath_aoi_check()

    download = download_data(
        path_to_cred_file = path_to_cred_file,
        log = log)
    download.download_sensat(
        uuid = uuid, title = title,
        download_path = download_path)
