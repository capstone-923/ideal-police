import csv
import json

def save_neighbourhood_data_to_csv(geojson_file, output_csv):
    """
    Save the neighbourhood mapping (ID, name, and coordinates) to a CSV file.

    :param geojson_file: Path to the GeoJSON file.
    :param output_csv: Path to the output CSV file.
    """
    # Extract the mapping list
    with open(geojson_file, 'r') as file:
        data = json.load(file)

    # Extract neighbourhood information (ID, name, coordinates)
    neighbourhood_data = []
    for feature in data['features']:
        properties = feature.get('properties', {})
        hood_id = properties.get('HOOD_ID')
        area_name = properties.get('AREA_NAME')
        geometry = feature.get('geometry')
        coordinates = geometry.get('coordinates', []) if geometry else None
        
        # Add to the list if valid
        if hood_id and area_name and coordinates:
            neighbourhood_data.append({
                'Neighbourhood ID': hood_id,
                'Neighbourhood Name': area_name,
                'Coordinates': coordinates
            })

    # Sort the data by Neighbourhood ID
    neighbourhood_data = sorted(neighbourhood_data, key=lambda x: x['Neighbourhood ID'])

    # Save to CSV
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['Neighbourhood ID', 'Neighbourhood Name', 'Coordinates'])
        writer.writeheader()
        writer.writerows(neighbourhood_data)

    print(f"Neighbourhood data has been saved to {output_csv}")


# Path to your GeoJSON file and output CSV
geojson_file = "../useful_data/Neighbourhood_Crime_Rates_Open_Data_-5291801778870948764.geojson"  # Replace with the actual GeoJSON file path
output_csv = "../useful_data/neighbourhood_data.csv"  # Replace with your desired output CSV file name

# Save the neighbourhood data to CSV
save_neighbourhood_data_to_csv(geojson_file, output_csv)
