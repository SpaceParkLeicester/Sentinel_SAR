import os
from google.cloud import storage

class gcp_bucket():
    """Function class for the earth data in GCP"""
    def __init__(
            self,
            bucket_name: str = None,
            location_name: str = None,
            granule: str = None,          
            log = None) -> None:
        """Declaring variables
        
        Args:
            bucket_name: Name of the bucket to search for
            location_name: Location name of the SAR data
            granule: Granule title of the SAR data, ends with '.SAFE'
            log: Custom logging function
        """
        self.bucket_name = bucket_name
        self.location_name = location_name
        self.granule = granule        
        self.log = log
        # Initiating the client
        self.client = storage.Client()
        
    def access_earthdata(self):
        """Accesing the Granule data"""

        # Checking if the bucket exists
        self.bucket = self.client.bucket(self.bucket_name)
        
        if self.bucket.exists():
            # Getting the blob names
            self.blobs = self.client.list_blobs(self.bucket_name)
            for blob in self.blobs:
                if self.location_name == blob.name.split('/')[0]:
                    if self.granule == blob.name.split('/')[1]:
                        self.granule_blobs = self.client.list_blobs(
                            self.bucket_name, 
                            prefix = f'{self.location_name}/{self.granule}/measurement')
                        return self.granule_blobs
                    else:
                        self.log.debug(f"{self.granule} does not exist in the {self.bucket_name}/{self.location_name}")
                else:
                    self.log.debug(f"{self.location_name} folder does not exist in {self.bucket_name}")
                    return None
        else:
            self.log.debug(f"bucket '{self.bucket_name}' does not exist")
            self.log.info("Create the bucket manually!")
    
    def read_tiff_file(
            self,
            required_tiff_file):
        """Reading the required tiff file into bytes"""
        # Getting the blob of required tiff file
        for granule_blob in self.granule_blobs:
            tiff_file = os.path.basename(granule_blob.name)
            tiff_file = tiff_file.split('.')[0]
            if tiff_file == required_tiff_file:
                # Getting the tiff file contents in bytes
                tiff_contents = granule_blob.download_as_bytes()
                return tiff_contents
        


