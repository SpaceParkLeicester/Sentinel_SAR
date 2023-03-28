"""Testing the fucntions of gcloud bucket"""
import os
from oil_storage_tanks.load import gcp_load_sar
from oil_storage_tanks.utils import gcp_bucket, logger

bucket_name = 's1-data'
location_name = 'Middlesbrough'
granule = 'S1A_IW_SLC__1SDV_20230315T062256_20230315T062324_047651_05B91D_320D.SAFE'
required_tiff_file = 's1a-iw1-slc-vh-20230315t062257-20230315t062322-047651-05b91d-001'

def test_read_earthdata_bucket():
    """Testing to read earth data from GCP bucket"""
    # Initialising the function
    gcp = gcp_bucket(bucket_name = bucket_name)
    granule_blobs = gcp.access_earthdata(
        location_name = location_name,
        granule = granule
    )
    assert granule_blobs is not None

    # Checking if it is  a tiff file
    for granule_blob in granule_blobs:
        _, file_ext = os.path.splitext(granule_blob.name)
        assert file_ext == '.tiff'

# def test_load_gcp_sar():
#     """Testing to load SAR data in GCP"""
#     # Initalising the bucket to the bucket filepaths
#     gcp = gcp_bucket(bucket_name = bucket_name)
#     granule_blobs = gcp.access_earthdata(
#         location_name = location_name,
#         granule = granule
#     )

#     # Loading the data for the required TIFF file
#     for file_path in granule_paths:
#         tiff_file = os.path.basename(file_path)
#         tiff_file = tiff_file.split('.')[0]
#         if tiff_file == required_tiff_file:
#             sar_data = gcp_load_sar(
#                 file_path = file_path
#             )
#             data = sar_data.load()
#             assert data is not None
