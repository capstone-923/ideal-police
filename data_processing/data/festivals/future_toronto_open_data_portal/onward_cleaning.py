#2
import json
import pandas as pd
from data_processing.data.festivals.future_toronto_open_data_portal.onward_extraction import *

# Function to extract the flattened record
def process_json(data: dict) -> list:
    """
    Processes a JSON record, flattening nested fields and generating rows for each 'dates' entry.

    Arguments:
    data: dict
        A dictionary representing a JSON record with fields such as 'dates', 'cost', 'features', and 'locations'.

    Functionality:
    - Extracts non-nested fields and adds them to the base record.
    - Flattens and includes nested fields from 'cost', 'features', and 'locations'.
    - Handles nested dictionaries within the 'locations' field, such as coordinates.
    - Generates separate rows for each entry in the 'dates' field, appending relevant datetime and description details.
    - Returns a list of rows, where each row is a dictionary representing a processed record.

    Returns:
    - rows: list of dict
        A list of flattened dictionaries, with one dictionary for each 'dates' entry (or a single dictionary if 'dates' is absent).
    """
    rows = []
    base_fields = {k: v for k, v in data.items() if k not in ['dates', 'cost', 'features', 'locations']}  # Exclude nested fields
    event_description = data.get('description', 'No description provided')
    base_fields['event_description'] = event_description
    # Process 'cost'
    if 'cost' in data:
        for key, value in data['cost'].items():
            base_fields[f'cost_{key}'] = value

    # Process 'features'
    if 'features' in data:
        for key, value in data['features'].items():
            base_fields[key] = value

    # Process 'locations' (only take the first location if multiple exist)
    if 'locations' in data and len(data['locations']) > 0:
        location = data['locations'][0]
        for key, value in location.items():
            if isinstance(value, dict):  # Handle nested location fields like 'coords'
                for sub_key, sub_value in value.items():
                    base_fields[f'{key}_{sub_key}'] = sub_value
            else:
                base_fields[key] = value

    # Process 'dates' to create separate rows
    if 'dates' in data:
        for date_entry in data['dates']:
            row = base_fields.copy()
            row['startDateTime'] = date_entry.get('startDateTime', None)
            row['endDateTime'] = date_entry.get('endDateTime', None)
            row['description_time'] = date_entry.get('description', None)
            rows.append(row)
    else:
        rows.append(base_fields)  # If no 'dates', keep a single row
    return rows

# Function to clean up `.000Z` in date fields
def clean_dates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans up `.000Z` in datetime fields of a DataFrame.

    Arguments:
    df: pd.DataFrame
        A Pandas DataFrame containing datetime columns to be cleaned.

    Functionality:
    - Looks for 'startDateTime' and 'endDateTime' columns in the DataFrame.
    - Removes the trailing '.000Z' from datetime strings in these columns.
    - Returns the cleaned DataFrame.

    Returns:
    - df: pd.DataFrame
        The modified DataFrame with cleaned datetime fields.
    """
    for col in ['startDateTime', 'endDateTime']:
        if col in df.columns:
            df[col] = df[col].str.replace('.000Z', '', regex=False)
    return df

def JSON2CSV(json_file: str) -> None:
    """
    Converts a JSON file of calendar events to a CSV file.

    Arguments:
    json_file: str
        The path to the JSON file containing calendar event data.

    Functionality:
    - Loads the JSON file and processes each calendar event in the 'calEvent' field.
    - Uses the `process_json` function to flatten nested structures and generate rows for each event.
    - Cleans up `.000Z` in datetime fields ('startDateTime' and 'endDateTime') using `clean_dates`.
    - Converts the processed data into a Pandas DataFrame and saves it as a CSV file.
    - The CSV file name includes the provided year and month.

    Returns:
    None
    """
    # Load JSON data
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Process each calendar event in the list
    all_rows = []  # List to store all processed rows
    for event in data:  # Iterate through each event in the list
        rows = process_json(event['calEvent'])  # Process the 'calEvent' part of the current event
        all_rows.extend(rows)  # Add the processed rows to the overall list

    # Convert to DataFrame
    df = pd.DataFrame(all_rows)

    # Clean up `.000Z` in datetime fields
    df = clean_dates(df)

    # Save to CSV using the current month
    df.to_csv(f'{data_year}{data_month}.csv', index=False)

    print(f"CSV file '{data_year}{data_month}.csv' has been created.")

def main():
    JSON2CSV(new_json_name)

if __name__ == "__main__":
    main()
        