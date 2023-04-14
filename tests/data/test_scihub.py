"""Testing the functions of the scihub"""
import os
from oil_storage_tanks.utils import logger
from oil_storage_tanks.data import AuthCredentials
from oil_storage_tanks.data.scihub import SearchSciHubData
from sentinelsat import SentinelAPI

def test_scihub_query():
    """Testing scihub authentication"""
    path_to_cred_file = '.private/cred.json'
    data_service = 'Copernicus scihub'
    if not os.path.exists(path_to_cred_file):
        username = os.environ.get('SCIHUB_USERNAME')
        password = os.environ.get('SCIHUB_PASSWORD')
        # Authenticating the username and password
        auth = AuthCredentials(
            username = username,
            password = password,
            log = logger())
        api = auth.scihub_auth()
        assert type(api) is SentinelAPI
    else:
        auth = AuthCredentials(
            path_to_cred_file = path_to_cred_file,
            data_service = 'Copernicus scihub',
            log = logger()
        )
        auth.credentials()
        api = auth.scihub_auth()
        assert type(api) is SentinelAPI

    """Testing scihub footprint"""
    half_side = 10
    location_name = 'stanlow'
    search = SearchSciHubData(
        data_service = data_service,
        path_to_cred_file = path_to_cred_file,
        log = logger())
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

