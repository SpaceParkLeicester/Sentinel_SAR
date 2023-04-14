"""Functions to test authentication"""
import os
from asf_search.ASFSession import ASFSession
from sentinelsat.sentinel import SentinelAPI
from oil_storage_tanks.data import AuthCredentials
from oil_storage_tanks.utils import logger

def test_earthdata_auth():
    """Testing earthdata credentials"""
    path_to_cred_file = ".private/cred.json"
    if not os.path.exists(path_to_cred_file):
        username = os.environ.get('EARTHDATA_USERNAME')
        password = os.environ.get('EARTHDATA_PASSWORD')
        # Authenticating the username and password
        auth = AuthCredentials(
            username = username,
            password = password,
            log = logger())
        user_session = auth.earthdata_auth()
        assert type(user_session) is ASFSession
    else:
        auth = AuthCredentials(
            path_to_cred_file = path_to_cred_file,
            data_service = 'NASA EARTHDATA',
            log = logger())
        auth.credentials()
        user_session = auth.earthdata_auth()
        assert type(user_session) is ASFSession


def test_scihub_auth():
    """Testing scihub credentials in github workflow"""
    path_to_cred_file = ".private/cred.json"
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
