import csv
import sys
import requests
import json
import regex as re
from datetime import datetime

def download_geojson(url, outupt_geojson):
    """
    Downloads a GeoJSON file from the given URL and saves it to a file.
    
    Args:
        url (str): The URL to download the GeoJSON file from.
        output_geojson (str): Path to save the downloaded GeoJSON file.
    """
    response = requests.get(url, output_geojson)
    if response.status_code == 200:
        with open(output_geojson, 'w', encoding='utf-8') as file:
            file.write(response.text)
        print(f"GeoJSON file downloaded and saved to {output_geojson}")
    else:
        print(f"Failed to download GeoJSON file. Status code: {response.status_code}")
        sys.exit(1)

def geojson_to_csv(input_geojson, output_csv):
    """
    Converts a GeoJSON file to a CSV file, transforming date fields from timestamps to readable dates.
    
    Args:
        input_geojson (str): Path to the input GeoJSON file.
        output_csv (str): Path to save the converted CSV file.
    """
    with open(input_geojson, 'r', encoding='utf-8') as file:
        geojson_data = json.load(file)

    features = geojson_data.get('features', [])
    if not features:
        print("No features found in the GeoJSON file.")
        sys.exit(1)

    # Extract field names from properties of the first feature
    fieldnames = features[0]['properties'].keys()

    # Write to CSV
    with open(output_csv, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for feature in features:
            row = feature['properties']
            # Convert timestamps to readable dates if present
            for key, value in row.items():
                if isinstance(value, int) and len(str(value)) >= 13:  # Likely a timestamp in milliseconds
                    try:
                        row[key] = datetime.utcfromtimestamp(value / 1000).strftime('%Y/%m/%d %H:%M:%S')
                    except Exception:
                        pass
            writer.writerow(row)

    print(f"CSV file created at {output_csv}")

if __name__ == "__main__":

    geojson_urls = ["https://services.arcgis.com/S9th0jAJ7bqgIRjw/arcgis/rest/services/Shooting_and_Firearm_Discharges_Open_Data/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson", "https://services.arcgis.com/S9th0jAJ7bqgIRjw/arcgis/rest/services/Homicides_Open_Data_ASR_RC_TBL_002/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson", "https://services.arcgis.com/S9th0jAJ7bqgIRjw/arcgis/rest/services/Assault_Open_Data/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson", "https://services.arcgis.com/S9th0jAJ7bqgIRjw/arcgis/rest/services/Auto_Theft_Open_Data/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson", "https://services.arcgis.com/S9th0jAJ7bqgIRjw/arcgis/rest/services/Bicycle_Thefts_Open_Data/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson", "https://services.arcgis.com/S9th0jAJ7bqgIRjw/arcgis/rest/services/Break_and_Enter_Open_Data/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson", "https://services.arcgis.com/S9th0jAJ7bqgIRjw/arcgis/rest/services/Robbery_Open_Data/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson", "https://services.arcgis.com/S9th0jAJ7bqgIRjw/arcgis/rest/services/Theft_Over_Open_Data/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson", "https://services.arcgis.com/S9th0jAJ7bqgIRjw/arcgis/rest/services/Theft_From_Motor_Vehicle_Open_Data/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson", "https://services.arcgis.com/S9th0jAJ7bqgIRjw/arcgis/rest/services/HATE_CRIME_OPEN_DATA/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson", "https://services.arcgis.com/S9th0jAJ7bqgIRjw/arcgis/rest/services/Traffic_Collisions_Open_Data/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"]

    for geojson_url in geojson_urls:
        match = re.search(r'/([^/]+)/FeatureServer', geojson_url)
        output_csv = f"{match.group(1)}.csv"
        output_geojson = f"{match.group(1)}.geojson"
        download_geojson(geojson_url, output_geojson)
        geojson_to_csv(output_geojson, output_csv)
