"""Test the utils functions"""
from shapely.wkt import loads
from oil_storage_tanks.data import OilTerminals

def test_oilterminals_dict():
    """Testing the oil terminal file"""
    terminal_data = OilTerminals()
    data = terminal_data.read_data()

    assert type(data) is dict
    assert data is not None

def test_bounding_box():
    """Testing the bounding box"""
    # Defining variables
    location_name = 'flotta'
    half_side = 50

    # Calling the bbox function
    terminal_data = OilTerminals(
        location_name = location_name,
        half_side = half_side)
    terminal_data.read_data()
    aoi_box = terminal_data.polygon_coords()
    poly = loads(aoi_box)

    assert poly.geom_type == 'Polygon'