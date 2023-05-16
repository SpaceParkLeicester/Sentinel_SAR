"""Test the utils functions"""
from shapely.wkt import loads
from shapely.geometry.polygon import Polygon
from src.data import OilTerminals

def test_oilterminals_dict():
    """Testing the oil terminal file"""
    csv_filepath = "data/oil_terminals_bbox.csv"
    terminal_data = OilTerminals()
    data = terminal_data.read_data()
    terminal_data.write_csv(filepath = csv_filepath)
    assert type(data) is dict
    assert data is not None

def test_bounding_box():
    """Testing the bounding box"""
    # Defining variables
    location_name = 'stanlow'
    half_side = 10

    # Calling the bbox function
    terminal_data = OilTerminals()
    data = terminal_data.read_data()
    aoi_box = terminal_data.bounding_box(
        center_lat = data[location_name][0],
        center_lon = data[location_name][1],
        half_side = half_side)
    poly = loads(aoi_box)

    assert type(poly) is Polygon