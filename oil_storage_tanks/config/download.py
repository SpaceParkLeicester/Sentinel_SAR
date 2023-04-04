"""Downloading data for the SAR pre-processing"""
from oil_storage_tanks.utils import logger
from oil_storage_tanks.data.asf_data import earthdata_auth, download_asf

class download_data(earthdata_auth):
    """Function to download single scene"""
    def __init__(
            self, 
            path_to_cred_file: str = None, 
            log=None) -> None:
        """Inherting from the auth function
        
        Args:
            path_to_cred_file: Path to the credentail file
            log: Custom logger function
        """
        super().__init__(path_to_cred_file, log)
        self.log = log
        self.user_pass_session = super().auth()
    
    def commence_download(
            self,
            download_path:str = None,
            csv_search_results_path:str = None)-> None:
        """Downloading one scene from the seacth results"""
        # Calling Download function
        data_download = download_asf(
            user_pass_session = self.user_pass_session,
            download_path = download_path,
            csv_search_results_path = csv_search_results_path,
            log = self.log
        )
        data_download.check_files()
        data_path = data_download.get_download_path()
        data_download.download_data()
        return data_path
        
if __name__ == "__main__":
    path_to_cred_file = '.private/earthdata_cred.json'
    download_path = 'data/SAFE'
    csv_seach_results_path = 'data/s1_data_search_results/Flotta/s1_Flotta_20230101_20230115.csv'
    dl = download_data(
        path_to_cred_file = path_to_cred_file,
        log = logger())
    dl.commence_download(
        download_path = download_path,
        csv_search_results_path = csv_seach_results_path)
