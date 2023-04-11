import rasterio
from rasterio.plot import show

def geotiff_viz(path):
    """Visualise GeoTiff images"""
    img = rasterio.open(path)
    show(img)

if __name__ == "__main__":
    path = 'data/pre_process/S1A_IW_GRDH_1SDV_20230301T175145_20230301T175210_047454_05B27C_E425_10.tif'
    geotiff_viz(path = path)