# Test to download the data
from oil_storage_tanks.utils import logger
from oil_storage_tanks.utils import gcp_earthdata
from oil_storage_tanks.data import bounding_box as bbox
from oil_storage_tanks.data import oil_terminals

def test_oilterminals_bbox():
    """Testing the oil terminal file and bounding box"""
    # Getting the full path of current directory
    terminal_file_path = "data/uk_oil_terminals.xlsx"    
    # Reading the data
    data = oil_terminals(
        terminal_file_path = terminal_file_path)
    for key, value in data.items():
        assert key is not None
        assert value is not None

        # Testing the bounding box
        bbox_aoi = bbox(
            center_lat = value[0],
            center_lon = value[1])
        assert bbox_aoi is not None

def test_read_gcp():
    """Testing the function to read from GCP"""
    bucket_name = "s1-data"
    filename = "test.csv"
    log = logger()
    gcp_data = gcp_earthdata(
        bucket_name = bucket_name,
        log = log
        )
    data = gcp_data.read_from_gcp(
        filename = filename
    )
    assert data is not None
    