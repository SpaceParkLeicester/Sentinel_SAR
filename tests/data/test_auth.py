"""Functions to test authentication"""
from oil_storage_tanks.data import auth_credentials

def test_scihub_auth():
    """Testing scihub credentials in github workflow"""
    scihub = auth_credentials()
    scihub.scihub_auth(
        username = scihub_username,
        password = scihub_password
    )