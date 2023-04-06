"""Functions to test authentication"""
import os
from oil_storage_tanks.data import auth_credentials

def test_scihub_auth():
    """Testing scihub credentials in github workflow"""
    username = os.environ.get('SCIHUB_USERNAME')
    password = os.environ.get('SCIHUB_PASSWORD')
    scihub = auth_credentials()
    scihub.scihub_auth(
        username = username,
        password = password
    )