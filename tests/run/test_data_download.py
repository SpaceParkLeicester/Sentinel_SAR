# Test to download the data
from oil_storage_tanks.run import DownloadS1Data

def test_download_s1_data():
    """Testing ASF download data"""
    # Source - https://github.com/asfadmin/Discovery-asf_search
    path_to_terminals = "Oil-Storage-Tanks/tests/data/uk_oil_terminals.xlsx"
    data = DownloadS1Data(path_to_terminals = path_to_terminals)