import json
from typing import Dict, List, Union, Optional


def neighbourhood_mapping_list(geojson_file: str) -> Dict[int, str]:
    """
    Returns a sorted dictionary where the keys are neighbourhood_id and the values are the corresponding neighbourhood_name.
    The dictionary is sorted by neighbourhood_id.

    :param geojson_file: Path to the GeoJSON file.
    :return: Sorted dictionary {neighbourhood_id: neighbourhood_name}.
    """
    with open(geojson_file, 'r') as file:
        data = json.load(file)

    mapping: Dict[int, str] = {}
    for feature in data['features']:
        properties = feature.get('properties', {})
        hood_id = properties.get('HOOD_ID')
        area_name = properties.get('AREA_NAME')
        if hood_id and area_name:
            mapping[hood_id] = area_name

    # Sort the dictionary by HOOD_ID and return
    return dict(sorted(mapping.items()))


def point_in_polygon(lat: float, long: float, polygon: List[List[float]]) -> bool:
    """
    Checks if a point is inside a polygon using the ray-casting algorithm.

    :param lat: Latitude of the point.
    :param long: Longitude of the point.
    :param polygon: List of [longitude, latitude] pairs representing the polygon.
    :return: True if the point is inside the polygon, False otherwise.
    """
    x, y = long, lat
    inside = False
    n = len(polygon)

    px1, py1 = polygon[0]
    for i in range(1, n + 1):
        px2, py2 = polygon[i % n]

        # Check if the point is exactly on the edge
        if min(px1, px2) <= x <= max(px1, px2) and min(py1, py2) <= y <= max(py1, py2):
            if (py2 - py1) * (x - px1) == (px2 - px1) * (y - py1):  # Check collinearity
                return True

        # Ray-casting logic
        if min(py1, py2) < y <= max(py1, py2) and x <= max(px1, px2):
            if py1 != py2:
                xinters = (y - py1) * (px2 - px1) / (py2 - py1) + px1
            if px1 == px2 or x <= xinters:
                inside = not inside

        px1, py1 = px2, py2

    return inside


def find_neighbourhood_id(lat: float, long: float, geojson_file: str) -> Optional[int]:
    """
    Accepts latitude and longitude as inputs and returns the neighbourhood_id that this latitude and longitude belongs to.

    :param lat: Latitude of the point.
    :param long: Longitude of the point.
    :param geojson_file: Path to the GeoJSON file.
    :return: Neighbourhood ID if the point is inside a neighbourhood, else None.
    """
    with open(geojson_file, 'r') as file:
        data = json.load(file)

    for feature in data['features']:
        geometry = feature.get('geometry')
        properties = feature.get('properties', {})
        if geometry and properties:
            if geometry['type'] == 'Polygon':
                for polygon in geometry['coordinates']:
                    if point_in_polygon(lat, long, polygon):
                        return properties.get('HOOD_ID')
            elif geometry['type'] == 'MultiPolygon':
                for multipolygon in geometry['coordinates']:
                    for polygon in multipolygon:
                        if point_in_polygon(lat, long, polygon):
                            return properties.get('HOOD_ID')

    return None
