import ee
import logging

log = logging.getLogger(__name__)

def ee_initiate(
        service_account: str = 'storage-tank@gy7720.iam.gserviceaccount.com',
        private_key:str = None
        )-> None:
    """Function to authenticate Earth Engine

        service_account = Name of the service account
        private_key = Path to the downloaded service account private key
    """
    credentials = ee.ServiceAccountCredentials(service_account, private_key)

    ee.Initialize(credentials)

    log.info("Earth Engine Initiation successful")
