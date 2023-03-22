import asf_search as asf
from oil_storage_tanks.utils import logger
from oil_storage_tanks.data.asf_data import (
    search_earthdata, 
    earthdata_auth)

def test_search():
    """Testing asf search for the default values"""
    # Initialising the function
    asf_data = search_earthdata(
        log = logger()
        )
    
    # Getting the metadata into a variable
    metadata = asf_data.metadata()

    assert metadata is not None

def test_auth():
    """Testing EARTH DATA authentication"""
    # Path to the cred file
    path_to_cred_file = ".private/earthdata_cred.json"
    check = earthdata_auth(
        path_to_cred_file = path_to_cred_file,
        log = logger())
    check = check.auth()
    assert type(check) == asf.ASFSession
