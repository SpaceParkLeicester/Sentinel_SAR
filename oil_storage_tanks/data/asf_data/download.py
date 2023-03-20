"""Function to download the ASFDATA"""
import os
import numpy as np
import json
import pandas as pd
from typing import Optional
from getpass import getpass
try:
    import asf_search as asf
    from oil_storage_tanks.utils import logger
except ImportError as e:
    import logging
    logging.debug(f"Import error: {e}")


class download_asf():
    """Functions relating to download data from ASF"""
    def __init__(
            self,
            path_to_cred_file: str = None) -> None:
        """Declaring variables
        
        Args:
            path_to_cred_file: Path to the crednetial file
        """
        self.path_to_cred_file = path_to_cred_file
        self.log = logger()
    
    def earthdata_auth(self) -> np.int64:
        """Authenticating the EARTHDATA login details"""
        # Checking the path to the credential file
        if not os.path.exists(self.path_to_cred_file):
            # Setting up the username and password
            earthdata_link = "https://www.earthdata.nasa.gov/"
            self.log.debug(f"For details, visit: {earthdata_link}")
            self.log.info("Enter you EARTHDATA username")
            username = input("Username:")
            self.log.info("Enter your EARTHDATA password")
            password = getpass("Password:")
        else:
            self.log.info("Getting info from the credential file")
            with open(self.path_to_cred_file) as f:
                earthdata = json.load(f)
                username = earthdata['username']
                password = earthdata['password']
                f.close()          

        try:
            self.user_pass_session = asf.ASFSession().auth_with_creds(
                username = username,
                password = password
            )
        except asf.ASFAuthenticationError as e:
            self.log.debug(f"Authentication failed:\n{e}")
            return 401
        else:
            self.log.info("User Authentication Successful!")
            return 235

    def download_data(
            self,
            search_results_path: str,
            download_path: str,
            download_single_file: Optional[bool] = True) -> None:
        """Function to download the data"""
        # Getting the URL's of the search result
        if not os.path.exists(search_results_path):
            self.log.debug("The search results csv does not exists!")
            self.log.debug("Check '~/oil_storage_tanks/data/asf_data/search.py'")
        else:
            search_results_df = pd.read_csv(search_results_path, header = 0)
            urls_df = search_results_df["URL"]
            granules_df = search_results_df["Granule Name"]
            self.log.info(f"Total number of URL's available are : {urls_df.shape[0]}")

            # Download the data of given urls
            urls_list = urls_df.values.tolist()
            granules_list = granules_df.values.tolist()

            # Download a single file
            if download_single_file:
                # Checking if the file exists
                filename = granules_list[0] + ".zip"
                if not os.path.exists(download_path, filename):
                    self.log.info(f"Commencing download of the file: {filename}")
                    url = urls_list[0]
                    asf.download_url(
                        url = url,
                        path = download_path,
                        filename = filename,
                        session = self.user_pass_session)
                else:
                    self.log.debug(f"{filename} already exists!")

if __name__ == "__main__":
    path_to_cred_file = "oiltanks/.private/earthdata_cred.json"
    search_results_path = "oiltanks/data/s1_data/s1_flotta_20230310_20230318.csv"
    download_path = "oiltanks/data/s1_data"

    download = download_asf(
        path_to_cred_file = path_to_cred_file
    )
    download.earthdata_auth()
    download.download_data()


