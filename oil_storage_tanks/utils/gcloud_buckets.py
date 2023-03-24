import os
from google.cloud import storage

    
class gcp_earthdata():
    """Function class for the earth data in GCP"""
    def __init__(
            self,
            bucket_name: str = None,
            log = None) -> None:
        """Declaring variables
        
        Args:
            bucket_name: Name of the bucket to search for
            file_path: Path to the files that needs uploading
            log: Custom logging function
        """
        self.bucket_name = bucket_name
        self.log = log
        # Initiating the client
        self.client = storage.Client()

        # Checking if the bucket exists
        self.bucket = self.client.bucket(self.bucket_name)
        try:
            self.bucket.exists()
            # Getting the blob names
            self.blobs = self.client.list_blobs(self.bucket_name)
            self.blob_names = [blob.name for blob in self.blobs]
        except Exception:
            self.log.debug(f"bucket{self.bucket_name} does not exist")
            self.log.info("Create the bucket manually!")
        
        
    def write_to_gcp(
            self,
            file_path:str = None)-> None:
        """Function to write the data into the bucket"""

        # Sanity check
        assert os.path.exists(file_path)

        # Checking if the download is already exists
        self.filename = os.path.basename(file_path)
        if self.filename in self.blob_names:
            self.log.debug(f"{self.filename} already exists in {self.bucket_name}")
        else:
            # Write the data into the the bucket
            self.log.info("Commencing the upload to the bucket")
            blob = self.bucket.blob(self.filename)
            blob.upload_from_filename(file_path)
            self.log.info("upload finished!")

    def read_from_gcp(
            self,
            filename:str = None):
        """Function to read data from GCP
        
        Args:
            filename: Name of the file that needs to be read
        """
        # Checking if the file exists in the cloud
        if filename in self.blob_names:
            self.log.info(f"Reading {filename} from {self.bucket_name} bucket")
            # Getting the blob 
            blob = self.bucket.blob(filename)
            # Reading the data
            with blob.open("r") as f:
                data = f.read()
                f.close()
            return data
        else:
            self.log.debug(f"{filename} does not exist in {self.bucket_name} bucket")
            return None



