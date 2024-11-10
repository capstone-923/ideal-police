import pandas as pd
import os

# Directory and output file paths
directory_path = '/home/ghamr/Downloads/'  # Replace with your directory path
output_file_path = 'summary_report.csv'  # Path for the output CSV file

# List to collect results
results = []

# Set to collect unique columns across all files
unique_columns = set()

# Identify unique columns from all CSV files
for file_name in os.listdir(directory_path):
    if file_name.endswith('.csv'):
        file_path = os.path.join(directory_path, file_name)
        df = pd.read_csv(file_path)
        unique_columns.update(df.columns)

# Convert the set to a list for processing
unique_columns = sorted(list(unique_columns))

# Define the regex term for column validation, ignoring '0', 'NA', 'NSA', and empty cells
# Special case for OFFENCE and PRIMARY_OFFENCE
regex_general = r'^(?!\s*$|0$|na$|nsa$|unknown$).*$'
regex_offence = r'^(?!\s*$|0$|na$|nsa$|assault$).*$'

# Function to process columns and count valid entries
def count_valid_entries(df, column, regex_term):
    if column in df.columns:
        series = df[column].astype(str).str.strip().str.lower()
        if regex_term:
            valid_entries = series[series.str.match(regex_term, na=False)]
        else:
            if column == 'occ_date' or column == 'report_date':
                series = pd.to_datetime(series, errors='coerce')
                valid_entries = series[series.dt.year >= 2000]
            else:
                valid_entries = series
        return valid_entries.count()
    return 0

# Load the CSV files and calculate the valid entries for each column
for file_name in os.listdir(directory_path):
    if file_name.endswith('.csv'):
        file_path = os.path.join(directory_path, file_name)
        df = pd.read_csv(file_path)

        # Dictionary to store findings for the current file
        file_summary = {
            'file_name': file_name
        }

        # Loop through each unique column
        for column in unique_columns:
            if column.lower() in ['offence', 'primary_offence']:
                # Apply special regex for OFFENCE/PRIMARY_OFFENCE (excluding 'Assault')
                count = count_valid_entries(df, column, regex_offence)
            else:
                # Apply general regex for all other columns
                count = count_valid_entries(df, column, regex_general)

            # Create a count key based on column name
            column_count_name = column
            file_summary[column_count_name] = count

        # Append the summary for the current file to the results list
        results.append(file_summary)

# Convert the list of dictionaries to a DataFrame
results_df = pd.DataFrame(results)

# Write the results to a CSV file
results_df.to_csv(output_file_path, index=False)

print(f"Summary report saved to {output_file_path}")