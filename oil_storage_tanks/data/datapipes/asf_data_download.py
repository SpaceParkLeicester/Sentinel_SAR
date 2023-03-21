from oil_storage_tanks.data.datapipes import search_results_datapipe
from oil_storage_tanks.utils import logger
from oil_storage_tanks.data.asf_data import download_asf

class download_all(search_results_datapipe):
    """Function to download all available csv files"""
    def __init__(
            self, 
            path_to_cred_file: str = None, 
            log=None, 
            path_to_uk_terminals: str = None, 
            csv_file_save_path: str = None, 
            download_path: str = None) -> None:
        super().__init__(
            path_to_cred_file, log, 
            path_to_uk_terminals, csv_file_save_path, 
            download_path)
        """Declaring variables"""
        self.path_to_cred_file = path_to_cred_file
        self.path_to_uk_terminals = path_to_uk_terminals
        self.csv_file_save_path = csv_file_save_path
        self.download_path = download_path
        self.log = logger()
    
    def commence_download(self) -> None:
        """Downloading data"""
        super().get_dictionary()
        csv_file_paths = super().write_search()
        for csv_filepath in csv_file_paths:
            download = download_asf(
                path_to_cred_file = self.path_to_cred_file,
                download_path = self.download_path,
                csv_search_results_path = csv_filepath)
            download.check_files()
            download.get_download_path()
            download.download_data()

if __name__ == "__main__":
    path_to_cred_file = ".private/earthdata_cred.json"
    path_to_uk_terminal = "data/uk_oil_terminals.xlsx"
    csv_file_save_path = "data/s1_data_search_results"
    download_path = "data/SAFE"
    download = download_all(
        path_to_cred_file = path_to_cred_file,
        path_to_uk_terminals = path_to_uk_terminal,
        csv_file_save_path = csv_file_save_path,
        download_path = download_path
        )
    download.commence_download()