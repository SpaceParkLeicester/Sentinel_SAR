from oil_storage_tanks.utils import gcp_bucket
import rioxarray as rxr
import gcsfs
import imageio
import matplotlib.pyplot as plt
import numpy as np
import skimage.io
import os
import PIL.Image

bucket_name = 's1-data'
location_name = 'Middlesbrough'
granule = 'S1A_IW_SLC__1SDV_20230315T062256_20230315T062324_047651_05B91D_320D.SAFE'
required_tiff_file = 's1a-iw1-slc-vh-20230315t062257-20230315t062322-047651-05b91d-001'

def colorize(z):
  n,m = z.shape

  A = (np.angle(z) + np.pi) / (2*np.pi)
  A = (A + 0.5) % 1.0 * 255
  B = 1.0 - 1.0/(1.0+abs(z)**0.3)
  B = abs(z)/ z.max() * 255
  H = np.ones_like(B)
  image = PIL.Image.fromarray(np.stack((A, B, np.full_like(A, 255)), axis=-1).astype(np.uint8), "HSV") # HSV has range 0..255 for all channels
  image = image.convert(mode="RGB")

  return np.array(image)

def test_gcp_load_sar():
    """Testing to load the SAR data from GCP"""
    # Getting the TIFF contents from GCP
    gcp = gcp_bucket(
        bucket_name = bucket_name,
        location_name = location_name,
        granule = granule)
    granule_blobs = gcp.access_earthdata()

    fs = gcsfs.GCSFileSystem('oil-storage-tank')
    for granule_blob in granule_blobs:
        if required_tiff_file == os.path.basename(granule_blob.name).split('.')[0]:
            imge_bytes = fs.cat(f'{bucket_name}/{granule_blob.name}')
            image = imageio.core.asarray(imageio.imread(imge_bytes, 'TIFF'))
            image = colorize(image)

            plt.figure(figsize=(10,10))
            skimage.io.imshow(image)