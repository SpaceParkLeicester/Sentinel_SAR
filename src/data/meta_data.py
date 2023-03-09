import ee
import os

key_path = os.path.join(os.getcwd(), 'gcp_key.json')
service_account = 'storage-tank@gy7720.iam.gserviceaccount.com'
credentials = ee.ServiceAccountCredentials(service_account, key_path)

ee.Initialize(credentials)