import os
from zipfile import ZipFile

def unzip_scihub_s1data(
        download_path:str = None,
        path_to_zip_file: str = None,
        unzip_dir_filename:str = None):
    """Unzip S1-data files
    
    Args:
        dowmload_path: Path to the zip file download
        path_to_zip_file: Path to file with .zip ext
        unzip_dir_file_name: Zip filename without .zip ext
    """
    unzip_dir_path = os.path.join(download_path, unzip_dir_filename)
    if not os.path.exists(unzip_dir_path):
        os.makedirs(unzip_dir_path)
        with ZipFile(path_to_zip_file, 'r') as zip_object:
            zip_object.extractall(unzip_dir_path)
        os.remove(path_to_zip_file)
    else:
        pass