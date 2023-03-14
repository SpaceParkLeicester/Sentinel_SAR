# Test to download the data
from oil_storage_tanks import DownloadS1Data

def test_download_s1_data():
    """Testing ASF download data"""
    # Source - https://github.com/asfadmin/Discovery-asf_search
    path_to_terminals = "Oil-Storage-Tanks/tests/data/uk_oil_terminals.xlsx"
    path_to_cred_file = "Oil-Storage-Tanks/earthdata_cred.json"
    data = DownloadS1Data(
        path_to_terminals = path_to_terminals,
        path_to_cred_file = path_to_cred_file)
    assert data is not None