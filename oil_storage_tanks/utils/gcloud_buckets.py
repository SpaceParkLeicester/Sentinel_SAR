import os
from google.cloud import storage
from oil_storage_tanks.utils import logger

    

def write_to_gcp(
        bucket_name: str = None,
        file_path: str = None,
        log = logger())-> None:
    """Function to write the data into the bucket
    
    Args:
        bucket_name: Name of the bucket
        file_path: Path to the local file
        log: Custom logging function
    """
    # Sanity check
    assert os.path.exists(file_path)

    # Check if the bucket exists
    log.info(f"Checking if the bucket{bucket_name} exists!")
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    if bucket.exists():
        log.info(f"{bucket_name} bucket exists")

        # Checking if the download is already exists
        filename = os.path.basename(file_path)
        blobs = client.list_blobs(bucket_name)
        blob_names = [blob.name for blob in blobs]
        if filename in blob_names:
            log.debug(f"{filename} already exists in {bucket_name}")
        else:
            # Write the data into the the bucket
            blob = bucket.blob(filename)
            blob.upload_from_filename(file_path)

def read_from_gcp(
        bucket_name: str = None,
        filename: str = None,
        log = logger()
        ):
    """Function to read data from GCP
    
    Args:
        bucket_name: Name of the bucket
        filename: Name of the file needed to be read
        log: Custom logger function
    """
    