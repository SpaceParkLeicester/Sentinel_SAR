"""Functions to test authentication"""
import logging
from logging import config
config.fileConfig('logger.ini')
logger = logging.getLogger(__name__)

from asf_search.ASFSession import ASFSession
from sentinelsat.sentinel import SentinelAPI
from src.data import AuthCredentials


def test_earthdata_auth():
    """Testing earthdata credentials"""
    auth = AuthCredentials(log = logger)
    user_session = auth.earthdata_auth()
    assert type(user_session) is ASFSession


def test_scihub_auth():
    """Testing scihub credentials in github workflow"""

    auth = AuthCredentials(log = logger)
    api = auth.scihub_auth()
    assert type(api) is SentinelAPI
