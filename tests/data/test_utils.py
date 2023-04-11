"""Test the utils functions"""
from shapely.wkt import loads
from oil_storage_tanks.data import oil_terminals, polygon_coords_csv
from oil_storage_tanks.data import bounding_box as bbox

def test_oilterminals_dict():
    """Testing the oil terminal file"""
    terminal_file_path = "data/uk_oil_terminals.xlsx"
    data = oil_terminals(
        terminal_file_path = terminal_file_path
    )
    assert type(data) is dict
    assert data is not None
    print(data)

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

def test_polygon_csv():
    """Testing csv file written with polygon wkt"""
    terminal_file_path = "data/uk_oil_terminals.xlsx"
    out_csv_file = 'data/uk_oil_termianls_poly.csv'
    half_side = 10
    df = polygon_coords_csv(
        terminal_file_path = terminal_file_path,
        out_csv_file = out_csv_file,
        half_side = half_side
        )
    assert df is not None