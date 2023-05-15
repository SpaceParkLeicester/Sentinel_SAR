from glob import glob
import asf_search as asf
from oil_storage_tanks.utils import logger
from oil_storage_tanks.data.asf_data import download_asf
from oil_storage_tanks.data import auth_credentials

class download_data():
    """Function to download all available csv files"""
    def __init__(
            self, 
            user_pass_session:asf.ASFSession = None, 
            bucket_name:str = None,            
            log=None, 
            path_to_uk_terminals: str = None, 
            csv_folder: str = None, 
            download_path: str = None) -> None:
        """Declaring variables"""
        self.user_pass_session = user_pass_session
        self.bucket_name = bucket_name
        self.path_to_uk_terminals = path_to_uk_terminals
        self.csv_folder = csv_folder
        self.download_path = download_path
        self.log = log
    
    def commence_download(self) -> None:
        """Downloading data"""
        csv_folders = glob(f'{csv_folder}/*/')
        for loc in csv_folders:
            csv_search_results_path = glob(loc+'/*.csv')
            for csv_file in csv_search_results_path:
                data = download_asf(
                    user_pass_session = self.user_pass_session,
                    download_path = self.download_path,
                    bucket_name = bucket_name,
                    csv_search_results_path = csv_file,
                    log = self.log)
                data.check_files()
                data.get_download_path()
                data.download_data()
                # data.zip_extract_earthdata()
                # data.upload_to_gcp()


if __name__ == "__main__":
    path_to_cred_file = ".private/cred.json"
    path_to_uk_terminal = "data/uk_oil_terminals.xlsx"
    bucket_name = "s1-data"
    download_path = "data/SAFE"    
    csv_folder = "data/s1_data_search_results"
    
    # Getting the session
    session = auth_credentials(
        path_to_cred_file = path_to_cred_file,
        log = logger())
    session.credentials()
    user_pass_session = session.earthdata_auth()

    # Downloading the data
    download = download_data(
        user_pass_session = user_pass_session,
        bucket_name = bucket_name,
        path_to_uk_terminals = path_to_uk_terminal,
        download_path = download_path,
        csv_folder = csv_folder,
        log = logger())
    download.commence_download()
