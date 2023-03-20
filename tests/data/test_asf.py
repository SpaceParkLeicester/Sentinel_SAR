from oil_storage_tanks.data.asf_data import (
    asf_search, 
    download_asf)

def test_asf_search():
    """Testing asf search for the default values"""
    # Initialising the function
    asf_data = asf_search()
    
    # Getting the metadata into a variable
    metadata = asf_data.metadata()

    assert metadata is not None

def test_asf_auth():
    """Testing EARTH DATA authentication"""
    # Path to the cred file
    path_to_cred_file = ".private/earthdata_cred.json"
    download = download_asf(path_to_cred_file = path_to_cred_file)
    auth = download.earthdata_auth()
    assert auth == 235 # Meaning authentication successful
