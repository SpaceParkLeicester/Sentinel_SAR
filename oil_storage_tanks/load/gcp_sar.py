import rioxarray as rxr
from io import BytesIO
from oil_storage_tanks.utils import gcp_bucket

class gcp_load_sar():
    """Functions to load the SAR data"""
    def __init__(
            self,
            file_contents: BytesIO = None) -> None:
        """Initalising the variables"""
        self.file_contents = file_contents
    
    def load(self):
        """Function to load the data"""
        dataset = rxr.open_rasterio(self.file_contents)
        metadata = dataset.rio.meta
        return metadata
    
