"""Function to download the ASFDATA"""
import os
import pandas as pd
from oil_storage_tanks.data.asf_data.auth import earthdata_auth

try:
    import asf_search as asf
    from oil_storage_tanks.utils import logger
except ImportError as e:
    import logging
    logging.debug(f"Import error: {e}")


class download_asf(earthdata_auth):
    """Functions relating to download data from ASF"""
    def __init__(self, path_to_cred_file: str = None) -> None:
        """ Initialising the logger"""        
        super().__init__(path_to_cred_file)
        self.user_pass_session = super().auth()
        self.log = logger()
    
    def check_files(
            self,
            search_results_path:str = None) -> bool:
        """Check if the file exists"""
        check = os.path.isfile(search_results_path) 
        if not check:
            self.log.debug("The search results csv does not exists!")
            self.log.debug("Check '~/oil_storage_tanks/data/asf_data/search.py'")
        
        return check

    def download_data(
            self,
            download_path: str = None) -> None:
        """Function to download the data"""

        # Getting the required info from the CSV file
        search_results_df = pd.read_csv(search_results_path, header = 0)
        urls_df = search_results_df["URL"] # URL
        granules_df = search_results_df["Granule Name"] # Granule name
        self.log.info(f"Total number of URL's available are : {urls_df.shape[0]}")

        # Converting the individual data into lists
        urls_list = urls_df.values.tolist()
        granules_list = granules_df.values.tolist()

        # Checking if the file exists
        # Downloading the first Granule in the search list
        filename = granules_list[0] + ".zip"
        filepath = os.path.join(download_path, filename)
        if not os.path.exists(filepath):
            self.log.info(f"Commencing download of the file: {filename}")
            url = urls_list[0]

            # Starting the download session
            asf.download_url(
                url = url,
                path = download_path,
                filename = filename,
                session = self.user_pass_session)
            self.log.info("Download is finished!")
        
        else:
            # If the file already exists
            self.log.debug(f"{filename} already exists!")

if __name__ == "__main__":
    path_to_cred_file = ".private/earthdata_cred.json"
    search_results_path = "data/s1_data/s1_flotta_20230310_20230318.csv"
    download_path = "data/s1_data/SAFE"

    download = download_asf(path_to_cred_file = path_to_cred_file)
    if download.check_files(
        search_results_path = search_results_path):
        download.download_data(
            download_path = download_path)

