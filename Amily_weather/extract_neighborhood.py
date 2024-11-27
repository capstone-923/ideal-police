import geojson
import pandas as pd

def read_geojson(file_path):
    """
    Reads a GeoJSON file and extracts information about neighborhoods.
    
    Args:
        file_path (str): Path to the GeoJSON file.
        
    Returns:
        pd.DataFrame: A dataframe containing the extracted information.
    """
    try:
        # Open and load the GeoJSON file
        with open(file_path, 'r') as f:
            data = geojson.load(f)
        
        # Extract information
        neighborhoods = []
        for feature in data['features']:
            area_code = feature['properties'].get('AREA_S_CD')
            area_name = feature['properties'].get('AREA_NAME')
            geometry = feature['geometry']
            neighborhoods.append({
                'Area Code': area_code,
                'Area Name': area_name,
                'Geometry Type': geometry['type'],
                'Coordinates': geometry['coordinates']
            })
        
        # Convert to DataFrame for analysis
        df = pd.DataFrame(neighborhoods)

        return df
    
    except Exception as e:
        print(f"Error reading GeoJSON file: {e}")
        return None

if __name__ == "__main__":
    # Change this path to your GeoJSON fil
    file_path = "./toronto_crs84.geojson"
    
    # Read the GeoJSON file
    df = read_geojson(file_path)
    
    if df is not None:
        print("GeoJSON data successfully read and processed!")
        print(df.head())  # Display the first few rows of the dataframe
        print(f"Total {len(df)} neighborhoods in toronto")
        df.to_csv("./toronto_neighborhood.csv", index=False)