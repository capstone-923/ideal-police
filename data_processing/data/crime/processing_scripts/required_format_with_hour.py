import csv
from datetime import datetime

def transform_csv(input_file, output_file, neighbourhood_mapping_file):
    """
    Transforms a CSV file to include Year, Month, Day, Hour, Neighbourhood Name, and Neighbourhood Number.
    Deletes the DIVISION column and keeps the OCC_HOUR column.

    Args:
        input_file (str): Path to the input CSV file.
        output_file (str): Path to the transformed CSV file.
        neighbourhood_mapping_file (str): Path to the CSV file containing neighbourhood names and numbers.
    """
    # Load neighbourhood mapping
    neighbourhood_mapping = {}
    with open(neighbourhood_mapping_file, mode='r', encoding='utf-8') as map_file:
        reader = csv.DictReader(map_file)
        headers = reader.fieldnames

        # Dynamically match headers for number and name
        number_col = next((col for col in headers if 'number' in col.lower()), None)
        name_col = next((col for col in headers if 'name' in col.lower()), None)

        if not number_col or not name_col:
            raise ValueError("Neighbourhood mapping file must contain columns for number and name.")

        for row in reader:
            neighbourhood_mapping[row[number_col]] = row[name_col]

    with open(input_file, mode='r', encoding='utf-8') as infile, \
         open(output_file, mode='w', encoding='utf-8', newline='') as outfile:

        reader = csv.DictReader(infile)
        fieldnames = ['Year', 'Month', 'Day', 'Hour', 'Neighbourhood Name', 'Neighbourhood Number'] + \
                     [col for col in reader.fieldnames if col not in ['DATE', 'DIVISION', 'HOOD_158']]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            # Parse the DATE column into Year, Month, and Day
            try:
                date_obj = datetime.strptime(row['DATE'], '%m/%d/%Y')
                row['Year'] = date_obj.year
                row['Month'] = date_obj.month
                row['Day'] = date_obj.day
            except ValueError:
                row['Year'] = row['Month'] = row['Day'] = None

            # Keep OCC_HOUR as Hour
            row['Hour'] = row['OCC_HOUR']

            # Map HOOD_158 to Neighbourhood Name and Number
            hood_number = row.get('HOOD_158', None)
            row['Neighbourhood Number'] = hood_number
            row['Neighbourhood Name'] = neighbourhood_mapping.get(hood_number, 'Unknown')

            # Remove unwanted columns
            for col in ['DATE', 'DIVISION', 'HOOD_158']:
                row.pop(col, None)

            writer.writerow(row)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python script.py <input_csv> <output_csv> <neighbourhood_mapping_csv>")
        sys.exit(1)

    input_csv = sys.argv[1]
    output_csv = sys.argv[2]
    neighbourhood_mapping_csv = sys.argv[3]
    transform_csv(input_csv, output_csv, neighbourhood_mapping_csv)
