import os
from tqdm import tqdm
from zipfile import ZipFile

def unzip_scihub_s1data(
        download_path:str = None,
        path_to_zip_file: str = None,
        unzip_dir_filename:str = None,
        log = None):
    """Unzip S1-data files
    
    Args:
        dowmload_path: Path to the zip file download
        path_to_zip_file: Path to file with .zip ext
        unzip_dir_file_name: Zip filename without .zip ext
    """
    unzip_dir_path = os.path.join(download_path, unzip_dir_filename + '.SAFE')
    if not os.path.exists(unzip_dir_path):
        log.info(f"Unzipping {unzip_dir_filename}")
        with ZipFile(path_to_zip_file, 'r') as zip_object:
            for file in tqdm(iterable = zip_object.namelist(), total = len(zip_object.namelist())):
                zip_object.extract(member = file, path = download_path)
            zip_object.close()
        log.info("Uzipping finished")
        log.info(f"Removing {path_to_zip_file}")
        os.remove(path_to_zip_file)
        return unzip_dir_path
    else:
        log.debug(f"{path_to_zip_file} already exists!")
        return unzip_dir_path