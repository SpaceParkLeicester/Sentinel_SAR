"""Test the utils functions"""
from shapely.wkt import loads
from oil_storage_tanks.data import oil_terminals
from oil_storage_tanks.data import bounding_box as bbox

def test_oilterminls_dict():
    """Testing the oil terminal file"""
    terminal_file_path = "data/uk_oil_terminals.xlsx"
    data = oil_terminals(
        terminal_file_path = terminal_file_path
    )
    assert type(data) is dict
    assert data is not None

def test_bounding_box():
    """Testing the bounding box"""
    # Loading the terminal data
    terminal_file_path = "data/uk_oil_terminals.xlsx"
    terminal_data = oil_terminals(
        terminal_file_path = terminal_file_path)
    
    # Getting the bounding box
    for _, coords in terminal_data.items():
        center_lat, center_lon = coords
        aoi_box = bbox(
            center_lat = center_lat,
            center_lon = center_lon,
            half_side = 10
        )
        poly = loads(aoi_box)

        assert poly.geom_type == 'Polygon'

       