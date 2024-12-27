#4
#drop necessary cols, expand the dates, and remove duplicating cols
import pandas as pd
from datetime import timedelta

input_csv = "gigantic.csv"

columns_to_drop = ['orgAddress','conv','type','description_time','orgPhoneExt','eventWebsite',
    'orgTypeOther','displayAddress','orgFax','eventPhoneExt','expectedAvg','coords','cost_child',
    'thumbImage','orgPhone','eventEmail','orgEmail','image','recId',
    'category','eventPhone','admin','contactTitle','locationType','id','$$hashKey',
    'weeklyDates','startDate','endDate','terms','partnerType','themeString','theme','orgName','contactName','geoCoded']
    #theme may can be deleted.

def remove_cols(input_csv: str) -> pd.DataFrame:
    """
    Removes specified columns from a CSV file and returns the resulting DataFrame.

    Arguments:
    input_csv: str
        The path to the input CSV file to process.
    columns_to_drop: list
        A list of column names to remove from the DataFrame.

    Functionality:
    - Reads the input CSV file into a Pandas DataFrame.
    - Drops the specified columns from the DataFrame.
    - Returns the modified DataFrame with the columns removed.

    Returns:
    - output_df: pd.DataFrame
        The resulting DataFrame with the specified columns removed.
    """
    input_df = pd.read_csv(input_csv)

    output_df = input_df.drop(columns=columns_to_drop)

    return output_df
  
#split date into three columns: year, month, and day
def dateExpansion(input_df: pd.DataFrame) -> pd.DataFrame:
    """
    Expands datetime columns into separate year, month, day, and time columns.

    Arguments:
    input_df: pd.DataFrame
        A Pandas DataFrame containing 'startDateTime' and 'endDateTime' columns with ISO 8601 timestamps.

    Functionality:
    - Cleans up '.000Z' from the datetime strings in 'startDateTime' and 'endDateTime'.
    - Extracts the year, month, day, and time components from each datetime column.
    - Drops the original 'startDateTime', 'endDateTime', and 'frequency' columns.
    - Returns the modified DataFrame with expanded datetime information.

    Returns:
    - output_df: pd.DataFrame
        The resulting DataFrame with separate columns for year, month, day, and time.
    """
    #Read the CSV file (replace 'file.csv' with your actual file path)

    # Split the timestamp into components
    input_df['startDateTime'] = input_df['startDateTime'].str.replace(".000Z", "", regex=False)  # Remove `.000Z`
    input_df['start_year'] = input_df['startDateTime'].str.slice(0, 4)  # Extract Year
    input_df['start_month'] = input_df['startDateTime'].str.slice(5, 7)  # Extract Month
    input_df['start_day'] = input_df['startDateTime'].str.slice(8, 10)  # Extract Day
    input_df['start_time'] = input_df['startDateTime'].str.slice(11)  # Extract Time

    # Split the timestamp into components
    input_df['endDateTime'] = input_df['endDateTime'].str.replace(".000Z", "", regex=False)  # Remove `.000Z`
    input_df['end_year'] = input_df['endDateTime'].str.slice(0, 4)  # Extract Year
    input_df['end_month'] = input_df['endDateTime'].str.slice(5, 7)  # Extract Month
    input_df['end_day'] = input_df['endDateTime'].str.slice(8, 10)  # Extract Day
    input_df['end_time'] = input_df['endDateTime'].str.slice(11)  # Extract Time
    # Drop the original timestamp column if not needed

    time_drop = ['startDateTime','endDateTime','frequency']

    output_df = input_df.drop(columns=time_drop)
    # Save to CSV
    return output_df

def verticalDateExpansion(input_df: pd.DataFrame) -> pd.DataFrame:
    """
    Expands rows of a DataFrame by generating a new row for each day within the start and end date range.

    Arguments:
    input_df: pd.DataFrame
        A Pandas DataFrame containing 'start_year', 'start_month', 'start_day', 
        'end_year', 'end_month', and 'end_day' columns.

    Functionality:
    - Converts start and end year-month-day columns into datetime objects.
    - Iterates through each row and generates rows for each day in the date range.
    - Expands date fields (day, month, year) for each generated row.
    - Removes duplicate rows and unnecessary columns for the final output.

    Returns:
    - expanded_input_df: pd.DataFrame
        A cleaned and expanded DataFrame with one row for each day the event spans.
    """
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

    df_cleaned_rows = df_cleaned_rows.drop(columns=['start_date', 'end_date','end_year','end_month','end_day'])

    #Produces the final cleaned dataset of 2014-2016
    df_cleaned_rows.to_csv('cleaned_dup_2017Mar_onward.csv', index=False)

    # Display the first few rows to check
    #print(expanded_input_df.head())

def main():
    process1=remove_cols(input_csv)
    process2=dateExpansion(process1)
    verticalDateExpansion(process2)

if __name__ == "__main__":
    main()
        
