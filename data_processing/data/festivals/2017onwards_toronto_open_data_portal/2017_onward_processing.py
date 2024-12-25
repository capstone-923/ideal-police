import json
import pandas as pd
from data_processing.data.festivals.2017onwards_toronto_open_data_portal.2017_onward_processing import *

# Function to extract the flattened record, splitting rows for 'dates'
def process_json(data):
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
def clean_dates(df):
    for col in ['startDateTime', 'endDateTime']:
        if col in df.columns:
            df[col] = df[col].str.replace('.000Z', '', regex=False)
    return df

def JSON2CSV(json_file)
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

    columns_to_drop = ['eventWebsite','thumbImage','orgPhone','eventEmail','orgEmail','image','recId',
    'category','eventPhone','admin','contactTitle','locationType','id','$$hashKey',
    'weeklyDates','startDate','endDate','terms','partnerType','themeString','theme','orgName','contactName','geoCoded']
    #theme may can be deleted.
    df = df.drop(columns=columns_to_drop)

    # Save to CSV using the current month
    df.to_csv(f'{data_year}{data_month}_super_clean.csv', index=False)

    print(f"CSV file '{data_year}{data_month}_super_clean.csv' has been created.")
