# Test to download the data
from oil_storage_tanks.utils import logger
from oil_storage_tanks.utils import oil_terminals
from oil_storage_tanks.utils import bounding_box as bbox
from oil_storage_tanks.utils import gcp_bucket

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

def test_logger():
    """Testing the logger function"""
    log = logger()
    log.info("This is the INFO message")
    log.debug("This is the DEBUG message")
    log.warning("This is the WARNING meassage")
    log.critical("This is the CRITICAL message")
    assert log is not None

def test_gcp_bucket():
    """Testing the gcp bucket functions"""
    bucket_name = 's1-data'
    location_name = 'Middlesbrough'
    granule = 'S1A_IW_SLC__1SDV_20230315T062256_20230315T062324_047651_05B91D_320D.SAFE'
    gcp = gcp_bucket(
        bucket_name = bucket_name,
        location_name = location_name,
        granule = granule        
        )
    data = gcp.access_earthdata()
    assert data is not None