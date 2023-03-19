"""Testing the Earthdata downloading"""
import os
from oil_storage_tanks.data import oil_terminals
import asf_search as asf
from oil_storage_tanks.data import s1_data_download

def test_earthdata_login_auth():    
    """Testing authentication"""
    # Getiing ASF data search function
    asf_data = s1_data_download()

    # Defining the path to crednetial file
    path_to_cred_file = ".private/earthdata_cred.json"
    if os.path.exists(path_to_cred_file):
        asf_data.earthdata_auth(
            earthdata_cred = path_to_cred_file)
    else:
        # Reading earth data credentials from json file
        username = os.environ.get('EARTHDATA_USERNAME')
        password = os.environ.get('EARTHDATA_PASSWORD')
    
        # Calling the ASF EARTHDATA API
        session = asf.ASFSession().auth_with_creds(username, password)
        assert session is not None

def test_metadata():
    """Testing the retreival of metadata"""
    # Reading the oil terminal xlsx file
    terminal_file_path = "data/uk_oil_terminals.xlsx"
    file_dict = oil_terminals(
        terminal_file_path = terminal_file_path)
    lat_lon = next(iter(file_dict.values()))

    # Getiing ASF data search function
    asf_data = s1_data_download()
    asf_meta = asf_data.s1_metadata(
        center_coords_lat = lat_lon[0],
        center_coords_lon = lat_lon[1])
    assert asf_meta is not None

