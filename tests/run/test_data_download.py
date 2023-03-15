# Test to download the data
import os
from oil_storage_tanks import DownloadS1Data
from oil_storage_tanks.data import bounding_box as bbox
from oil_storage_tanks.data import oil_terminals

def test_oilterminals():
    """Testing the oil terminal file"""
    # Getting the full path of current directory
    current_dir = os.path.dirname(__file__)
    parent_dir = os.path.dirname(os.path.abspath(current_dir)) 
    file_path = "data/uk_oil_terminals.xlsx"
    terminal_file_path = os.path.join(parent_dir, file_path)
    
    # Reading the data
    data = oil_terminals(
        terminal_file_path = terminal_file_path)
    assert data is not None

def test_earthdata_login_auth():    
    """Testing authentication"""
    pass

# def test_download_s1_data():
#     """Testing ASF download data"""
#     # Source - https://github.com/asfadmin/Discovery-asf_search
#     path_to_terminals = "Oil-Storage-Tanks/tests/data/uk_oil_terminals.xlsx"
#     path_to_cred_file = "Oil-Storage-Tanks/earthdata_cred.json"
#     download_path = "Oil-Storage-Tanks/tests/data"
#     data = DownloadS1Data(
#         path_to_terminals = path_to_terminals,
#         path_to_cred_file = path_to_cred_file,
#         download_path = download_path,
#         commence_download = True)
#     assert data is not None

