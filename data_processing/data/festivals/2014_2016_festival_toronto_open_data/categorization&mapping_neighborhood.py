#mapping daily + neighboor id (geographical location): number of each type of event and number of each trait of each type of event and free or not
import pandas as pd
from datetime import timedelta
from data_processing.data_utils.utils import *

neighborhood_geo="Neighbourhood_Crime_Rates_Open_Data_-5291801778870948764.geojson" #replace with the full path of where 
#the neighborhood geojson file is located on user's personal laptop
input = "cleaned_dup_2014_2016.csv" # replace with wherever the user stored the dataset outputted from 2014_2016_process.py
uncat_file ="need_AI_help_2014_2016.csv"
uncat_file_after_manual_categorization = "2014_2016_manual_done.csv"
cat_file = "ready_mapping_14_16.csv"
merged_file = "merged_14_16.csv"


def separation_cat_noncat(input_file, uncategorized_file,categorized_file):
    input_df = pd.read_csv(input_file, encoding='latin-1')

    # Extract uncategorized events
    uncategorized = input_df[
        (input_df['CategoryList'] == "") | 
        (input_df['txtLong'].isna()) | 
        (input_df['txtLat'].isna())
    ][['EventName', 'CategoryList', 'LongDesc']]

    # Save uncategorized events to a separate file
    uncategorized.to_csv(uncategorized_file, index=False)

    categorized = input_df[(input_df['CategoryList'] != "")&(input_df['txtLong'].notna()) & 
    (input_df['txtLat'].notna())]

    categorized.to_csv(categorized_file, index=False)

def combine_after_cat(input_file1,input_file2, output_file):
    input1 = pd.read_csv(input_file1, encoding='latin-1')
    input2 = pd.read_csv(input_file2, encoding='latin-1')

    final_df = pd.concat([input1, input2], ignore_index=True)

    #for debugging to visualize the resultant CSV. 
    final_df.to_csv(output_file, index=False)
    #return final_df

def mapping_neighborhood(input_file, neighborhood_geojson,Dict):
    input_df = pd.read_csv(input_file,index_col=False)

    output_df = input_df.copy()
    output_df['neighborhood_id'] = None
    output_df['neighborhood_name'] = None

    for index, rows in input_df.iterrows():
        neighborhood_id=find_neighbourhood_id(rows['txtLat'],rows['txtLong'],neighborhood_geojson)

        # Check if neighborhood_id is None before accessing the dictionary
        if neighborhood_id is not None:  
            neighborhood_name = Dict.get(neighborhood_id) # Use Dict.get to handle missing keys
            output_df.at[index, 'neighborhood_id'] = neighborhood_id
            output_df.at[index, 'neighborhood_name'] = neighborhood_name
            print(f"We are getting sth at index:" + str(index))
        else:
            # Handle cases where neighborhood_id is None (e.g., print a message)
            print(f"Warning: Event at index {index} has no neighborhood ID (lat: {rows['txtLat']}, long: {rows['txtLong']})")

    # Save mapped events to a separate file CSV for debugging visualization
    # output_df.to_csv(output_file, index=False)

    return output_df


def date_neighboorhood_count(input_data):

    # Combine 'day', 'month', and 'year' columns into a single 'date' column
    input_data['start_year'] = pd.to_numeric(input_data['start_year'], errors='coerce')
    input_data['start_month'] = pd.to_numeric(input_data['start_month'], errors='coerce')
    input_data['start_day'] = pd.to_numeric(input_data['start_day'], errors='coerce')

    input_data['date'] = pd.to_datetime(
        input_data[['start_year', 'start_month', 'start_day']].rename(
            columns={'start_year': 'year', 'start_month': 'month', 'start_day': 'day'}
        ),
        errors='coerce'
    )

    # Dynamically identify all unique categories in the dataset
    unique_categories = input_data['CategoryList'].unique()

        # Create aggregation rules for all categories
    aggregation_rules = {
        str(cat).replace(" ", "_"): ('CategoryList', lambda x, c=cat: (x == c).sum())
        for cat in unique_categories
    }
    # Group and aggregate
    result = (
        input_data.groupby(['date', 'neighborhood_name','neighborhood_id'])
        .agg(**aggregation_rules)
        .reset_index()
    )

    # Flatten the multi-level column names after pivot
    result.columns = ['_'.join(col).strip('_') if isinstance(col, tuple) else col for col in result.columns]

    # Dynamically identify all event count columns
    count_columns = [col for col in result.columns if col not in ['date', 'neighborhood_id','neighborhood_name', 'free_events']]
    
    # Ensure all count columns are numeric
    count_columns = [col for col in count_columns if pd.api.types.is_numeric_dtype(result[col])]  

    # Calculate the total number of events as the sum of all event count columns
    result['total_events'] = result[count_columns].sum(axis=1)

    # Split the 'date' column back into 'day', 'month', and 'year'
    result['year'] = result['date'].dt.year
    result['month'] = result['date'].dt.month
    result['day'] = result['date'].dt.day

    # Drop the original 'date' column if it's no longer needed
    result = result.drop(columns=['date'])

    # Save the categorized aggregated data to a file
    columns_front = ['neighborhood_name','neighborhood_id','year','month','day','total_events']
    columns_back = [col for col in result.columns if col not in columns_front]

    # Build the new column order
    new_order = columns_front + columns_back

    result = result[new_order]
    # Print confirmation messages

    # Save the categorized aggregated data to a file
    result.to_csv("neighborhood_attached_14_16.csv", index=False)

def main():

    Dict = neighbourhood_mapping_list(neighborhood_geo)
    separation_cat_noncat(input,uncat_file,cat_file)
    combine_after_cat(uncat_file,cat_file,merged_file)
    process1 = mapping_neighborhood(cat_file, neighborhood_geo,Dict)
    process2=date_neighboorhood_count(process1)


if __name__ == "__main__":
    main()