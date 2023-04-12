import snappy
import numpy as np
# import matplotlib.pyplot as plt
from snappy import ProductIO

def vis_sar(path_to_file):
    # Load the image using snappy
    df = ProductIO.readProduct(path_to_file)

    # Getting data from band
    band = df.getBand('Sigma0_VH_db') # Assign Band to a variable
    w = df.getSceneRasterWidth() # Get Band Width
    h = df.getSceneRasterHeight() # Get Band Height 
    print(w,h)
    # # Create an empty array
    # band_data = np.zeros(w * h, np.float32)
    # # Populate array with pixel value
    # band.readPixels(0, 0, w, h, band_data) 
    # # Reshape
    # band_data.shape = h, w
    # # Plot the band  
    # plt.figure(figsize=(18,10))
    # plt.imshow(band_data, cmap = plt.cm.binary)
    # plt.show()      
if __name__ == "__main__":
    path_to_file = 'data/SAFE/flotta_10.dim'
    vis_sar(path_to_file = path_to_file)