from oil_storage_tanks.utils import gcp_bucket
from oil_storage_tanks.load import gcp_load_sar

bucket_name = 's1-data'
location_name = 'Middlesbrough'
granule = 'S1A_IW_SLC__1SDV_20230315T062256_20230315T062324_047651_05B91D_320D.SAFE'
required_tiff_file = 's1a-iw1-slc-vh-20230315t062257-20230315t062322-047651-05b91d-001'

def test_gcp_load_sar():
    """Testing to load the SAR data from GCP"""
    # Getting the TIFF contents from GCP
    gcp = gcp_bucket(
        bucket_name = bucket_name,
        location_name = location_name,
        granule = granule)
    gcp.access_earthdata()
    tiff_contents = gcp.read_tiff_file(
        required_tiff_file = required_tiff_file
    )
    # Loading the GCP SAR data
    data = gcp_load_sar(file_contents = tiff_contents)
    data = data.load()
    assert data is not None