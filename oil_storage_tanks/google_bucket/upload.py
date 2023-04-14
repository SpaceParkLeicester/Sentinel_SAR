import os
import shutil
import subprocess as sp
from google.cloud import storage
from google.api_core.exceptions import NotFound

class GoogleBuckets:
    """Class function related to Google Buckets"""
    def __init__(
            self,
            local_filepath: str = None,
            bucket_path:str = None,
            log: isinstance = None) -> None:
        """Initiating Google Client
        
        Args:
            local_filepath: Relative path of the file needs to be uploaded
            bucket_path: bucket path of the file uploading
            log: instance of custom logger function
        """
        self.log = log
        self.local_filepath = local_filepath
        self.bucket_path = bucket_path
        self.client = storage.Client()
    
    def upload(self)-> None:
        """Uploading to the GCP buckets"""
        # Getting the filename
        self.filename = os.path.basename(self.local_filepath)
        self.abs_filepath = os.path.join(os.getcwd(), self.local_filepath)

        if os.path.exists(self.abs_filepath):
            # Listing files in the bucket
            self.bucket_name = self.bucket_path.split('/')[0]
            self.blobs = self.client.list_blobs(self.bucket_name)
            try:
                self.bucket_files = [blob.name.split('/')[-1] for blob in self.blobs]
            except NotFound:
                self.log(f"bucket{self.bucket_name} is not found in GCP")
            else:
                if self.filename not in self.bucket_files:
                    self.log.info(f"file {self.filename} not found in GCP")
                    self.log.info("Commencing upload!")
                    # Uploading file
                    sp.check_call(f'gsutil cp {self.abs_filepath} gs://{self.bucket_path}', 
                                shell = True, stdout = sp.PIPE)
                    self.log.info("Upload finished")
                else:
                    self.log.debug(f"{self.filename} exists in GCP")
        else:
            self.log.debug(f"file {self.local_filepath} does not exist")

    def remove_uploaded_files(self)-> None:
        """Removing files from local system"""
        # Removing file
        if os.path.exists(self.abs_filepath):
            shutil.rmtree(self.abs_filepath, ignore_errors = True)
        else:
            self.log.debug(f"file {self.abs_filepath} does not exist")



        