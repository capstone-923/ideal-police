import pytest
from data_processing.data_utils import utils
import json
import tempfile
from typing import Dict, List

# Helper function to create a temporary GeoJSON file for testing
def create_temp_geojson(features: List[Dict]) -> str:
    geojson_data = {
        "type": "FeatureCollection",
        "features": features
    }
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".geojson")
    with open(temp_file.name, 'w') as file:
        json.dump(geojson_data, file)
    return temp_file.name

# Test for neighbourhood_mapping_list
def test_neighbourhood_mapping_list():
    features = [
        {
            "type": "Feature",
            "properties": {"HOOD_ID": 2, "AREA_NAME": "Neighbourhood B"},
            "geometry": None
        },
        {
            "type": "Feature",
            "properties": {"HOOD_ID": 1, "AREA_NAME": "Neighbourhood A"},
            "geometry": None
        },
        {
            "type": "Feature",
            "properties": {"HOOD_ID": 3, "AREA_NAME": "Neighbourhood C"},
            "geometry": None
        }
    ]
    geojson_file = create_temp_geojson(features)

    result = utils.neighbourhood_mapping_list(geojson_file)
    expected = {1: "Neighbourhood A", 2: "Neighbourhood B", 3: "Neighbourhood C"}
    
    assert result == expected, f"Expected {expected}, got {result}"

# Test for point_in_polygon
@pytest.mark.parametrize("lat, long, polygon, expected", [
    (1, 1, [[0, 0], [2, 0], [2, 2], [0, 2]], True),   # Point inside square
    (3, 3, [[0, 0], [2, 0], [2, 2], [0, 2]], False),  # Point outside square
    (2, 2, [[0, 0], [2, 0], [2, 2], [0, 2]], True),   # Point on edge
    (0, 0, [[0, 0], [2, 0], [2, 2], [0, 2]], True),   # Point on vertex
    (1.5, 1.5, [[0, 0], [1, 2], [2, 1]], True),       # Point inside triangle
])
def test_point_in_polygon(lat, long, polygon, expected):
    result = utils.point_in_polygon(lat, long, polygon)
    assert result == expected, f"Point ({lat}, {long}) in {polygon} expected {expected}, got {result}"

# Test for find_neighbourhood_id
def test_find_neighbourhood_id():
    features = [
        {
            "type": "Feature",
            "properties": {"HOOD_ID": 1, "AREA_NAME": "Neighbourhood A"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[0, 0], [2, 0], [2, 2], [0, 2], [0, 0]]]
            }
        },
        {
            "type": "Feature",
            "properties": {"HOOD_ID": 2, "AREA_NAME": "Neighbourhood B"},
            "geometry": {
                "type": "MultiPolygon",
                "coordinates": [
                    [[[3, 3], [5, 3], [5, 5], [3, 5], [3, 3]]]
                ]
            }
        }
    ]
    geojson_file = create_temp_geojson(features)

    # Test point in Neighbourhood A
    assert utils.find_neighbourhood_id(1, 1, geojson_file) == 1

    # Test point in Neighbourhood B
    assert utils.find_neighbourhood_id(4, 4, geojson_file) == 2

    # Test point outside all neighbourhoods
    assert utils.find_neighbourhood_id(6, 6, geojson_file) is None
