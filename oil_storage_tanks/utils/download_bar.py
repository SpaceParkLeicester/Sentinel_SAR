import os
import numpy as np
from tqdm import tqdm
import time

def progress_bar(
        total_file_size: np.float64 = None,
        file_path: str = None
        ):
    """Function to get see the progress bar for ASF data download"""
    current_file_size = 0
    with tqdm(total = total_file_size, unit = 'MB', unit_scale = True) as pbar:
        while current_file_size < total_file_size:
            current_file_size = os.path.getsize(file_path) / 1024 * 1024
            pbar.update(current_file_size - pbar.n)
            time.sleep(1)
