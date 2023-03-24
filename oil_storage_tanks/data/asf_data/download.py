"""Function to download the ASFDATA"""
import os
from tqdm import tqdm
import subprocess
import time 
import logging
import pandas as pd
from google.cloud import storage
import zipfile
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
            bucket_name:str = None,            
            csv_search_results_path:str = None,          
            log = None) -> None:
        """ Initialising the logger"""        
        super().__init__(
            path_to_cred_file, log)
        self.log = log
        self.bucket_name = bucket_name
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
            self.log.debug("Run '~/oil_storage_tanks/data/asf_data/search.py'")
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
        self.filename = self.loc_name + "_" + self.granules_list[0] 
        self.filename_ext = self.filename + ".zip"
        self.filepath = os.path.join(self.download_path, self.filename_ext)
    
    def download_data(self)-> None:
        """Commencing the download"""
        # Checking if the file already exists in GCP bucket
        self.client = storage.Client()
        blobs = self.client.list_blobs(self.bucket_name)
        folder_list = [blob.name.split('/')[0] for blob in blobs]
        self.check = self.filename in folder_list
        if not self.check: 
            # If it does not exist in GCP bucket
            self.log.info(f"Commencing download of the file: {self.filename_ext}")
            url = self.urls_list[0]

            # Starting the download session
            asf.download_url(
                url = url,
                path = self.download_path,
                filename = self.filename_ext,
                session = self.user_pass_session)
            time.sleep(5)
            self.log.info("Download is finished!")
        else:
            self.log.debug(f"{self.filename} already exists in {self.bucet_name} bucket")
    
    def zip_extract_earthdata(self)-> None:
        """Extract the zipped data"""
        if not zipfile.is_zipfile(self.filepath):
            self.log.debug(f"{self.filepath} is not a zip file")
        else:
            with zipfile.ZipFile(self.filepath, 'r', allowZip64 = True) as zip_ref:
            # Extracting each member of the zip file
                self.log.info(f"Extracting data from {self.filename_ext}")                
                for file in tqdm(iterable = zip_ref.namelist(), total = len(zip_ref.namelist())):
                    zip_ref.extract(member = file, path = self.download_path)
                self.log.info("Extaction complete")
                zip_ref.close()

            # Deleting the zip file
            self.log.info(f"Removing the zip file: {self.filename_ext}")
            time.sleep(5)
            os.remove(self.filepath)
    
    def upload_files_to_gcp(self)-> None:
        """Upload files from local to GCP"""
        if os.path.exists(self.filename_ext):
            self.log.debug(f"{self.filename_ext} has not been completely removed!")
            self.log.debug("Make sure to remove the file to clear memory for other downloads")
        if not self.check:
            filepath = os.path.join(self.download_path, self.filename)
            self.log.info("Commencing upload to the bucket")
            subprocess.check_call(f'gsutil cp -r $PWD/{filepath} gs://{self.bucket_name}/')
            time.sleep(5)
            self.log.info("Upload finished!")
        else:
            self.log.debug(f"{self.filename} already exists in the bucket!")

        