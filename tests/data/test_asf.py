"""Testing the functions of ASF EARTHDATA"""
import logging
from logging import config
config.fileConfig('logger.ini')
logger = logging.getLogger(__name__)

from src.data.asf_data import SearchEarthData



def test_search():
    """Testing asf search for the default values"""
    # Initialising the function
    asf_data = SearchEarthData(log = logger)
    
    # Getting the metadata into a variable
    metadata = asf_data.metadata(half_side = 50)

    assert metadata is not None

