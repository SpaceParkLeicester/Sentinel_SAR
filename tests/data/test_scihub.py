from oil_storage_tanks.utils import logger
from oil_storage_tanks.data.scihub import search_data
from oil_storage_tanks.data import oil_terminals

def test_check_name():
    """Check the location name"""
    location_name = 'flotta'
    terminal_file_path = 'data/uk_oil_terminals.xlsx'
    oil_dict = oil_terminals(
        terminal_file_path = terminal_file_path)
    for loc_name, _ in oil_dict.items():
        if location_name == loc_name:
            print("location is present")
            break
        else:
            print("Location is not present")

def test_scihub_api():
    """Testing the scihub api"""
    data_service = "copernicus scihub"
    path_to_cred_file = '.private/cred.json'
    half_side = 10
    location_name = 'flotta'
    terminal_file_path = 'data/uk_oil_terminals.xlsx'
    start_date = '2023-03-01'
    end_date ='2023-03-30'

    # Initiaitng the function
    scihub = search_data(
        data_service = data_service,
        path_to_cred_file = path_to_cred_file,
        log = logger()
    )
    # Getting the footprint
    scihub.footprint(
        half_side = half_side,
        location_name = location_name,
        terminal_file_path = terminal_file_path
        )

    # SentinelAPI querying
    scihub.query(
        start_date = start_date,
        end_date = end_date
    )
    _ , uuid= scihub.swath_aoi_check()
    assert uuid is not None