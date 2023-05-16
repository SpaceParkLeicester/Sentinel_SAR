"""Testing the functions of the scihub"""
from src.data import AuthCredentials
from src.data.scihub import SearchSciHubData
from sentinelsat import SentinelAPI

import logging
from logging import config
config.fileConfig('logger.ini')
logger = logging.getLogger(__name__)

def test_scihub_query():
    """Testing scihub authentication"""

    auth = AuthCredentials(log = logger)
    api = auth.scihub_auth()
    assert type(api) is SentinelAPI

    """Testing scihub footprint"""
    half_side = 10
    location_name = 'stanlow'
    search = SearchSciHubData(log = logger)
    foot_print = search.footprint(
        half_side = half_side,
        location_name = location_name)
    assert foot_print is not None

    """Testing the search results"""
    start_date = '2023-03-01'
    end_date = '2023-03-09'
    df = search.query(
        start_date = start_date,
        end_date = end_date)
    assert df is not None

    title, _ = search.swath_aoi_check()
    assert title is not None

