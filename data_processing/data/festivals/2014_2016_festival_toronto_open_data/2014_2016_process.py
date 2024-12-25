import pandas as pd
from datetime import timedelta

input_CSV="cleaned_2014_2016.csv" #whatever name the user named output from 2014_2016_cleaning.py
merge_column = "CategoryList"
columns_to_remove = [
        "Exhibit", "Performance", "PresentedByOrgName", "OrgContactPhone", "OrgContactExt",
        "MapAddress", "EventURL", "ImageAltText", "OrgContactEMail", "txtGeoId", "TTC_2",
        "Address_2", "txtGeoId_2", "txtLong_2", "txtLat_2", "$21", "$22", "LocationType_2",
        "NumberLocations", "LocationType_1", "Location_1", "$13", "$14", "TTC_1",
        "Address_1", "txtGeoId_1", "txtLong_1", "txtLat_1"
    ]

def processCSV(input_file):
    # Define the column to merge and the columns to remove

    # Read the CSV file into a pandas DataFrame
    input_df = pd.read_csv(input_file, encoding='latin-1')
      
    if merge_column not in input_df.columns:
        input_df[merge_column] = ""  # Add the column if it doesn't exist
    # Fill the merge column based on conditions
    for index, row in input_df.iterrows(): # Unpack the tuple into index and row
    # Combine Exhibit and Performance columns into Category
      category_value = str(row.get(merge_column, "")).strip()  
      exhibit_value = str(row.get("Exhibit", "")).strip().lower()  
      performance_value = str(row.get("Performance", "")).strip().lower()  

      if not category_value:  # Check if Category is empty
        if exhibit_value == "exhibit":
          category_value = "Art/Exhibits"
        elif performance_value == "performance":
          category_value = "Live performance"

        # Update the row in the DataFrame (using .loc)
        input_df.loc[index, merge_column] = category_value 

    # Drop unwanted columns
    input_df = input_df.drop(columns=[col for col in columns_to_remove if col in input_df.columns])

    # Write the updated DataFrame to a new CSV file
    # Uncomment for debugging use to visualize the processed CSV stage 1
    #input_df.to_csv("test_panda.csv",index=False)

    # Uncomment for debugging 
    #print(f"Updated CSV file written to test_panda.csv")
    return input_df

def dateExpansion(input_df):

  # Ensure the start and end date columns are in datetime format
  input_df['DateBeginShow'] = pd.to_datetime(input_df['DateBeginShow'],format='mixed')
  input_df['DateEndShow'] = pd.to_datetime(input_df['DateEndShow'], format='mixed')

  # Split start_date into day, month, and year
  input_df['start_day'] = input_df['DateBeginShow'].dt.day.fillna(-1).astype(int)  # Fill NaT with -1 and then convert to int
  input_df['start_month'] = input_df['DateBeginShow'].dt.month.fillna(-1).astype(int)  # Fill NaT with -1 and then convert to int
  input_df['start_year'] = input_df['DateBeginShow'].dt.year.fillna(-1).astype(int)  # Fill NaT with -1 and then convert to int

  # Split end_date into day, month, and year
  input_df['end_day'] = input_df['DateEndShow'].dt.day.fillna(-1).astype(int)  # Fill NaT with -1 and then convert to int
  input_df['end_month'] = input_df['DateEndShow'].dt.month.fillna(-1).astype(int)  # Fill NaT with -1 and then convert to int
  input_df['end_year'] = input_df['DateEndShow'].dt.year.fillna(-1).astype(int)  # Fill NaT with -1 and then convert to int


  # Drop the original date columns if not needed
  # input_df = input_df.drop(columns=['start_date', 'end_date'])
  input_df = input_df.drop(columns=['DateBeginShow', 'DateEndShow'])

  # Reorder columns: Insert new columns into the desired positions
  # Move start_day, start_month, start_year to column 5
  start_cols = ['start_day', 'start_month', 'start_year']
  end_cols = ['end_day', 'end_month', 'end_year']

  # Get remaining columns
  remaining_cols = [col for col in input_df.columns if col not in (start_cols + end_cols)]

  # Build the new column order
  new_order = remaining_cols[:4] + start_cols + remaining_cols[4:5] + end_cols + remaining_cols[5:]

  # Reorder the DataFrame columns
  input_df = input_df[new_order]

  #for debugging to check if the current dataframe is expanded correctly
  #input_df.to_csv('expanded_2014_2016.csv', index=False) 
  return input_df

def fullDates(input_df):
  # Read the original CSV file (replace with your actual file path)


  # Convert start and end date columns into datetime objects
  input_df['start_date'] = pd.to_datetime(input_df[['start_year', 'start_month', 'start_day']].rename(columns={'start_year': 'year', 'start_month': 'month', 'start_day': 'day'}), errors='coerce')
  input_df['end_date'] = pd.to_datetime(input_df[['end_year', 'end_month', 'end_day']].rename(columns={'end_year': 'year', 'end_month': 'month', 'end_day': 'day'}), errors='coerce')

  # List to store the expanded rows
  expanded_rows = []

  # Iterate through each row of the DataFrame
  for _, row in input_df.iterrows():
      start_date = row['start_date']
      end_date = row['end_date']

      # Generate a new row for each day the event spans
      current_date = start_date
      while current_date <= end_date:
          # Create a copy of the original row and update the dates
          new_row = row.copy()  # Copy original row

          # Set the current date as both the start and end date for this row
          new_row['start_date'] = current_date
          new_row['end_date'] = current_date

          # Split the current date into day, month, and year for start_date
          new_row['start_day'] = current_date.day
          new_row['start_month'] = current_date.month
          new_row['start_year'] = current_date.year

          # Split the current date into day, month, and year for end_date (which is the same for now)
          new_row['end_day'] = current_date.day
          new_row['end_month'] = current_date.month
          new_row['end_year'] = current_date.year

          # Append the new row to the list of expanded rows
          expanded_rows.append(new_row)

          # Increment the current date by one day
          current_date += timedelta(days=1)

  # Create a new DataFrame with the expanded rows
  expanded_input_df = pd.DataFrame(expanded_rows)

  df_cleaned_rows = expanded_input_df.drop_duplicates()

  df_cleaned_rows = df_cleaned_rows.drop(columns=['start_date', 'end_date'])

  #Produces the final cleaned dataset of 2014-2016
  df_cleaned_rows.to_csv('cleaned_dup_2014_20161.csv', index=False)

  # Display the first few rows to check
  print(expanded_input_df.head())
  

def main():
    process1=processCSV(input_CSV)
    process2=dateExpansion(process1)
    fullDates(process2)


if __name__ == "__main__":
    main()