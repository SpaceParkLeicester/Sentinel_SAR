import click
from oil_storage_tanks.utils import logger, unzip_scihub_s1data
from oil_storage_tanks.data.scihub import search_data, download_data
from oil_storage_tanks.config import pre_process

@click.command()
@click.option('--data_service', type = str, default = 'Copernicus Scihub', help = 'Enter the type of service, EARTHDATA or Scihub')
@click.option('--user_name', type = str, help = 'Enter the username')
@click.option('--password', type = str, help = 'Enter the password')
@click.option('--start_date', type = str, help = 'Enter the start date of the search')
@click.option('--end_date', type = str, help = 'Enter the last date of the search')
@click.option('--half_side', type = int, help = 'Enter the half side of the desired AOI')
@click.option('--location_name', type = str, help = 'Enter the name of the oil terminal location')
@click.option('--platformname', type = str, default = 'Sentinel-1', help = 'Enter the Platform name, eg: Sentinel-1')
@click.option('--producttype', type = str, default = 'GRD', help = 'Enter the type of the prodyct, eg: SLC, GRD')
@click.option('--download_path', type = click.Path(exists = True), default = 'data/SAFE', help = 'Enter the download path for S1 zip files')
@click.option('--processed_folder', type = click.Path(exists = True), default = 'data/pre_process', help = 'Enter the path for the processed GeoTiff files')
@click.option('--terminal_file_path', type = click.Path(exists = True), default = 'data/uk_oil_terminals.xlsx', help = 'Path to the oil terminal xlsx data file')
def copernicus_data_download(
    user_name, password,
    start_date, end_date,
    half_side, location_name,
    data_service, platformname,
    producttype, terminal_file_path,
    download_path, processed_folder,
    log = logger()):
    """Datapipe to download a single scene"""

    # pipeline for the seacrh query
    scihub = search_data(
        data_service = data_service,
        username = user_name,
        password = password,
        log = log
    )
    wkt_string = scihub.footprint(
        half_side = half_side,
        location_name = location_name,
        terminal_file_path = terminal_file_path
    )
    scihub.query(
        start_date = start_date,
        end_date = end_date,
        platformname = platformname,
        producttype = producttype
    )
    title, uuid = scihub.swath_aoi_check()

    # pipeline for the download
    download = download_data(
        data_service = data_service,
        username = user_name,
        password = password,
        log = log
    )
    path_to_zip_file = download.download_sensat(
        uuid = uuid,
        title = title,
        download_path = download_path
    )

    # Extracting data
    grd_folder_path = unzip_scihub_s1data(
        download_path = download_path,
        path_to_zip_file = path_to_zip_file,
        unzip_dir_filename = title,
        log = log)

    # pre-processing
    preprocess = pre_process(
        grd_folder_path = grd_folder_path,
        processed_folder = processed_folder,
        wkt_string = wkt_string,
        log = log)
    preprocess.collect_data()
    preprocess.polarisation()
    preprocess.start_preprocess()
    preprocess.downsample()
    preprocess.geotiff_conversion()

if __name__ == "__main__":
    copernicus_data_download()