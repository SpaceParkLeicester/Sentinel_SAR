# Test to download the data
import os
import json
import asf_search as asf
# from oil_storage_tanks import DownloadS1Data
from oil_storage_tanks.data import bounding_box as bbox
from oil_storage_tanks.data import oil_terminals

def test_oilterminals():
    """Testing the oil terminal file"""
    # Getting the full path of current directory
    terminal_file_path = "tests/data/uk_oil_terminals.xlsx"    
    # Reading the data
    data = oil_terminals(
        terminal_file_path = terminal_file_path)
    for key, value in data.items():
        assert key is not None
        assert value is not None

def test_earthdata_login_auth():    
    """Testing authentication"""
    username = os.environ['EARTHDATA_USERNAME']
    password = os.environ['EARTHDATA_PASSWORD']    
    session = asf.ASFSession().auth_with_creds(username, password)
    assert session is not None

