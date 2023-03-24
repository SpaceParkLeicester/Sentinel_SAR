from glob import glob
from oil_storage_tanks.utils import logger
from oil_storage_tanks.data.asf_data import download_asf

class download_all():
    """Function to download all available csv files"""
    def __init__(
            self, 
            path_to_cred_file: str = None, 
            bucket_name:str = None,            
            log=None, 
            path_to_uk_terminals: str = None, 
            csv_folder: str = None, 
            download_path: str = None) -> None:
        """Declaring variables"""
        self.path_to_cred_file = path_to_cred_file
        self.bucket_name = bucket_name
        self.path_to_uk_terminals = path_to_uk_terminals
        self.csv_folder = csv_folder
        self.download_path = download_path
        self.log = log
    
    def commence_download(self) -> None:
        """Downloading data"""
        csv_file_paths = glob(self.csv_folder + '/*.csv')
        for csv_file in csv_file_paths:
            data = download_asf(
                path_to_cred_file = self.path_to_cred_file,
                download_path = self.download_path,
                bucket_name = bucket_name,
                csv_search_results_path = csv_file,
                log = self.log)
            data.check_files()
            data.get_download_path()
            data.download_data()
            data.zip_extract_earthdata()
            data.upload_files_to_gcp()


if __name__ == "__main__":
    path_to_cred_file = ".private/earthdata_cred.json"
    path_to_uk_terminal = "data/uk_oil_terminals.xlsx"
    csv_folder = "data/s1_data_search_results"
    bucket_name = "s1-data"
    download_path = "data/SAFE"    
    csv_folder = "data/s1_data_search_results"
    download = download_all(
        path_to_cred_file = path_to_cred_file,
        bucket_name = bucket_name,
        path_to_uk_terminals = path_to_uk_terminal,
        download_path = download_path,
        csv_folder = csv_folder,
        log = logger())
    download.commence_download()