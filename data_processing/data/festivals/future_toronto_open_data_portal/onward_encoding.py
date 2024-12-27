#5
import pandas as pd
from data_processing.data_utils.utils import *

# File paths
neighborhood_geo="Neighbourhood_Crime_Rates_Open_Data_-5291801778870948764.geojson" #replace with the full path of where 
#the neighborhood geojson file is located on user's personal laptop

input_file = "17Mar_onward.csv"  # Replace with your file name
output_file = "categorized_17Mar_onward.csv"
uncategorized_file = "need_AI_help_2017Mar_onward.csv"
uncat_file_after_manual_categorization = "2014_2016_manual_done.csv"
cat_file = "cat_17Mar_onward.csv"
merged_file = "merged_17Mar_onward.csv"

def categorize_event(row: pd.Series) -> str:
    """
    Categorizes an event based on its 'categoryString' field by checking predefined categories.
    
    Arguments:
    row: pd.Series
        A single row from a DataFrame containing an event's 'categoryString' field, 
        which holds a comma-separated string of categories.

    Returns:
    str
        A category label based on predefined categories or the first category in the list if no match is found.
    """
    # Split the category string and clean up spaces
    categories = row['categoryString'].split(",")
    categories = [cat.strip().lower() for cat in categories]

    # Check for predefined categories first
    if any("arts/exhibits" in cat for cat in categories):
        return "Arts/Exhibits"
    elif any("live performances" in cat for cat in categories) or any(cat in ["music", "theatre"] for cat in categories):
        return "Live Performances"
    elif any("sports" in cat for cat in categories):
        return "Sports_Game_To_Watch"
    elif any("seminars/workshops" in cat for cat in categories):
        return "Seminars/Workshops"
    elif any("street festival" in cat for cat in categories):
        return "Street Festival"
    elif any('celebrations/holiday' in cat for cat in categories):
        return "Celebrations/Holiday"
    elif any (["running", "walking", "hiking",'running/walking/hiking','cycling'] for cat in categories):
        return "Exercise"
    elif any("food/culinary"in cat for cat in categories):
        return "Food/Culinary"
    elif any("family/children"in cat for cat in categories):
       return "Family/Children"
    elif any("museum" in cat for cat in categories):
        return "Museum"
    elif any("dance" in cat for cat in categories):
        return "Dance"
    elif any('history' in cat for cat in categories):
        return "History"
    elif any('film' in cat for cat in categories):
        return "Film"
    elif any('tour' in cat for cat in categories):
        return "Tour"
    else:
        # If no predefined category matches, take the first category from the string
        return categories[0] if categories else "Uncategorized"

def combineDate(input_csv: str) -> pd.DataFrame:
    """
    Combines the 'start_year', 'start_month', and 'start_day' columns into a single 'date' column
    and returns the updated DataFrame.

    Arguments:
    input_csv: str
        The path to the input CSV file containing 'start_year', 'start_month', and 'start_day' columns.

    Returns:
    pd.DataFrame
        A DataFrame with an additional 'date' column that combines the year, month, and day into a datetime format.
    """

    # Read the CSV
    df = pd.read_csv(input_csv)

    # Combine 'day', 'month', and 'year' columns into a single 'date' column
    df['start_Year'] = pd.to_numeric(df['start_year'], errors='coerce')
    df['start_Month'] = pd.to_numeric(df['start_month'], errors='coerce')
    df['start_Day'] = pd.to_numeric(df['start_day'], errors='coerce')

    df['date'] = pd.to_datetime(
        df[['start_Year', 'start_Month', 'start_Day']].rename(
            columns={'start_Year': 'year', 'start_Month': 'month', 'start_Day': 'day'}
        ),
        errors='coerce'
    )

    return df

def separate_cat_noncat(input_df: pd.DataFrame, uncat: str, cat: str) -> None:
    """
    Separates categorized and uncategorized events from the input DataFrame and saves them to separate CSV files.

    Arguments:
    input_df: pd.DataFrame
        The input DataFrame containing event data, which must include the columns: 'categoryString', 
        'coords_lng', and 'coords_lat'.
    
    uncat: str
        The file path where uncategorized events (with missing category or coordinates) will be saved.

    cat: str
        The file path where categorized events (with non-empty category and valid coordinates) will be saved.

    Returns:
    None
        The function saves the categorized and uncategorized events as separate CSV files.
    """

    # Extract uncategorized events
    uncat = input_df[
        (input_df['categoryString'] == "") | 
        (input_df['coords_lng'].isna()) | 
        (input_df['coords_lat'].isna())
    ][['eventName', 'categoryString', 'event_description','coords_lng','coords_lat']]

    # Save uncategorized events to a separate file
    uncat.to_csv(uncategorized_file, index=False)

    # Filter out uncategorized events for aggregation
    categorized = input_df[(input_df['categoryString'] != "")&(input_df['coords_lng'].notna()) & 
    (input_df['coords_lat'].notna())]

    categorized.to_csv(cat, index=False)

def combine_after_cat(input_file1: str, input_file2: str, output_file: str) -> None:
    """
    Combines two CSV files into a single CSV file by concatenating them.

    Arguments:
    input_file1: str
        The file path of the first input CSV file.
    
    input_file2: str
        The file path of the second input CSV file.

    output_file: str
        The file path where the combined CSV will be saved.

    Returns:
    None
        The function saves the combined DataFrame as a new CSV file.
    """
    input1 = pd.read_csv(input_file1, encoding='latin-1')
    input2 = pd.read_csv(input_file2, encoding='latin-1')

    final_df = pd.concat([input1, input2], ignore_index=True)

    #for debugging to visualize the resultant CSV. 
    final_df.to_csv(output_file, index=False)
    #return final_df

def mapping_neighborhood(input_df: pd.DataFrame, neighborhood_geojson: dict, Dict: dict) -> pd.DataFrame:
    """
    Maps neighborhood information to a DataFrame based on geographic coordinates (latitude and longitude) and a geoJSON file.

    Arguments:
    input_df: pd.DataFrame
        The DataFrame containing event information, including latitude and longitude columns ('coords_lat' and 'coords_lng').
    
    neighborhood_geojson: dict
        A geoJSON object containing neighborhood boundaries and IDs.
    
    Dict: dict
        A dictionary mapping neighborhood IDs to neighborhood names.

    Returns:
    pd.DataFrame
        The updated DataFrame with added columns 'neighborhood_id' and 'neighborhood_name'.
    """

    output_df = input_df.copy()
    output_df['neighborhood_id'] = None
    output_df['neighborhood_name'] = None

    for index, rows in input_df.iterrows():
        neighborhood_id=find_neighbourhood_id(rows['coords_lat'],rows['coords_lng'],neighborhood_geojson)

        # Check if neighborhood_id is None before accessing the dictionary
        if neighborhood_id is not None:  
            neighborhood_name = Dict.get(neighborhood_id) # Use Dict.get to handle missing keys
            output_df.at[index, 'neighborhood_id'] = neighborhood_id
            output_df.at[index, 'neighborhood_name'] = neighborhood_name
            print(f"We are getting sth at index:" + str(index))
        else:
            # Handle cases where neighborhood_id is None (e.g., print a message)
            print(f"Warning: Event at index {index} has no neighborhood ID (lat: {rows['coords_lat']}, long: {rows['coords_lat']})")

    # Save mapped events to a separate file CSV for debugging visualization
    # output_df.to_csv(output_file, index=False)

def encode(input_df: pd.DataFrame, output_final: str):
    """
    Processes and categorizes events in the DataFrame, aggregates the data by neighborhood and date, 
    and then saves the results to a CSV file.

    Arguments:
    input_df: pd.DataFrame
        A DataFrame containing event information, including event category, date, and neighborhood data.
    
    output_file: str
        The path where the aggregated and categorized result will be saved as a CSV file.
    
    Returns:
    None
    """

    # Apply the categorization logic
    input_df['category'] = input_df.apply(categorize_event, axis=1)
    unique_categories = input_df['category'].unique()

    # Create aggregation rules for all categories
    aggregation_rules = {
        cat.replace(" ", "_"): ('category', lambda x, c=cat: (x == c).sum())
        for cat in unique_categories
    }

    # Add rule for free events 17_19
    aggregation_rules['free_events'] = ('freeEvent', lambda x: x.sum() if x.dtype == 'bool' else (x == 'Yes').sum())

    # Group and aggregate
    result = (
        input_df.groupby(['date', 'neighborhood_name','neighborhood_id'])
        .agg(**aggregation_rules)
        .reset_index()
    )

    # Flatten the multi-level column names after pivot
    result.columns = ['_'.join(col).strip('_') if isinstance(col, tuple) else col for col in result.columns]

    # Dynamically identify all event count columns
    count_columns = [col for col in result.columns if col not in ['date', 'neighborhood_name','neighborhood_id', 'free_events']]

    # Calculate the total number of events as the sum of all event count columns
    result['total_events'] = result[count_columns].sum(axis=1)

    # Split the 'date' column back into 'day', 'month', and 'year'
    result['year'] = result['date'].dt.year
    result['month'] = result['date'].dt.month
    result['day'] = result['date'].dt.day

    # Drop the original 'date' column if it's no longer needed
    result = result.drop(columns=['date'])

    columns_front = ['neighborhood_name','neighborhood_id','year','month','day','total_events','free_events']
    columns_back = [col for col in result.columns if col not in columns_front]

    # Build the new column order
    new_order = columns_front + columns_back

    result = result[new_order]
    # Print confirmation messages

    # Save the categorized aggregated data to a file
    result.to_csv(output_final, index=False)

def main():

    Dict = neighbourhood_mapping_list(neighborhood_geo)
    separate_cat_noncat(input,uncategorized_file,cat_file)

    '''Uncomment and proceed to running the following sections after manually input categories for the uncategorized CSV'''
    # combine_after_cat(uncat_file_after_manual_categorization,cat_file,merged_file)
    # process1=combineDate(merged_file)
    # process2 = mapping_neighborhood(process1, neighborhood_geo,Dict)
    # encode(process2,"2017Mar_onward_encoding.csv")

if __name__ == "__main__":
    main()