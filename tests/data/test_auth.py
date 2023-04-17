"""Functions to test authentication"""
from asf_search.ASFSession import ASFSession
from sentinelsat.sentinel import SentinelAPI
from oil_storage_tanks.data import AuthCredentials
from oil_storage_tanks.utils import logger

def test_earthdata_auth():
    """Testing earthdata credentials"""
    auth = AuthCredentials(log = logger())
    user_session = auth.earthdata_auth()
    assert type(user_session) is ASFSession


def test_scihub_auth():
    """Testing scihub credentials in github workflow"""

    auth = AuthCredentials(log = logger())
    api = auth.scihub_auth()
    assert type(api) is SentinelAPI

def test_planet_api():
    """Testing Planet authentication"""
    auth = AuthCredentials(log = logger())
    api = auth.planet_auth()
    assert api == 200