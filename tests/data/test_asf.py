from oil_storage_tanks.utils import logger
from oil_storage_tanks.data.asf_data import SearchEarthData
from pprint import pprint


def test_search():
    """Testing asf search for the default values"""
    # Initialising the function
    asf_data = SearchEarthData(log = logger())
    
    # Getting the metadata into a variable
    metadata = asf_data.metadata(half_side = 50)

    assert metadata is not None
    pprint(metadata)
