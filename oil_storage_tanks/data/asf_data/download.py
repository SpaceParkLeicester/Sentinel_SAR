"""Function to download the ASFDATA"""
import os
import subprocess
import time 
import logging
import pandas as pd
from oil_storage_tanks.data.asf_data.auth import earthdata_auth

try:
    import asf_search as asf
    from oil_storage_tanks.utils import logger
except ImportError as e:
    logging.debug(f"Import error: {e}")


class download_asf(earthdata_auth):
    """Functions relating to download data from ASF"""
    def __init__(
            self, 
            path_to_cred_file: str = None,
            download_path: str = None,
            csv_search_results_path:str = None,          
            log = None) -> None:
        """ Initialising the logger"""        
        super().__init__(
            path_to_cred_file, log)
        self.log = log
        self.download_path = download_path
        self.csv_search_results_path = csv_search_results_path      

        # Sanity check
        try:
            self.user_pass_session = super().auth()
            assert type(self.user_pass_session) == asf.ASFSession
        except AssertionError as e:
            self.log.debug(f"Resolve the bug: {e}")

    def check_files(self) -> bool:
        """Check if the file exists"""
        check = os.path.isfile(self.csv_search_results_path) 
        if not check:
            self.log.debug("The search results csv does not exists!")
            self.log.debug("Check '~/oil_storage_tanks/data/asf_data/search.py'")
        else:
            basename = os.path.basename(self.csv_search_results_path)
            self.loc_name = os.path.splitext(basename)[0]
            self.loc_name = self.loc_name.split('_')[1]

    def get_download_path(self) -> None:
        """Function to download the data"""
        # Getting the required info from the CSV file
        search_results_df = pd.read_csv(self.csv_search_results_path, header = 0)
        self.urls_df = search_results_df["URL"] # URL
        self.granules_df = search_results_df["Granule Name"] # Granule name
        self.log.info(f"Total number of URL's available are : {self.urls_df.shape[0]}")

        # Converting the individual data into lists
        self.urls_list = self.urls_df.values.tolist()
        self.granules_list = self.granules_df.values.tolist()

        # Checking if the file exists
        # Downloading the first Granule in the search list
        self.filename = self.loc_name + "_" + self.granules_list[0] + ".zip"
        self.filepath = os.path.join(self.download_path, self.filename)
    
    def download_data(self):
        """Commencing the download"""
        if not os.path.exists(self.filepath):
            self.log.info(f"Commencing download of the file: {self.filename}")
            url = self.urls_list[0]

            # Starting the download session
            asf.download_url(
                url = url,
                path = self.download_path,
                filename = self.filename,
                session = self.user_pass_session)
            self.log.info("Download is finished!")

            # Moving the file to GCP bucket
            # Bash script to move files to GCP
            time.sleep(5)
            bash_script = "oil_storage_tanks/utils/move_to_gc.sh"
            subprocess.run(["bash", bash_script])

            # Remove the file
            time.sleep(5)
            self.log.info(f"Removing the file: {self.filename} from folder")
            os.remove(self.filepath)
            
            # Sanity check
            try:
                check = os.path.exists(self.filepath)
                assert check == False
            except AssertionError as e:
                self.log.debug(f"{self.filename} has not be completely removed!")
        
        else:
            # If the file already exists
            self.log.debug(f"{self.filename} already exists!")