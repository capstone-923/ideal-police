import pandas as pd
import os

# Directory and output file paths
directory_path = '/home/ghamr/Downloads/'  # Replace with your directory path
output_repeated_file_path = 'summary_report_repeated.csv'  # Path for the repeated columns output CSV file
output_non_repeated_file_path = 'summary_report_non_repeated.csv'  # Path for the non-repeated columns output CSV file

# List to collect results for repeated and non-repeated columns
results_repeated = []
results_non_repeated = []

# Dictionary to count occurrences of each column across all files
column_counts = {}

# Identify columns from all CSV files and count occurrences
file_count = 0
for file_name in os.listdir(directory_path):
    if file_name.endswith('.csv'):
        file_count += 1
        file_path = os.path.join(directory_path, file_name)
        df = pd.read_csv(file_path)
        
        # Update column counts for each column in the file
        for column in df.columns:
            column_counts[column] = column_counts.get(column, 0) + 1

# Separate columns into two sets: repeated across all files and not repeated
repeated_columns = set([col for col, count in column_counts.items() if count == file_count])
non_repeated_columns = set([col for col, count in column_counts.items() if count < file_count])

# Sort columns for consistency
repeated_columns = sorted(list(repeated_columns))
non_repeated_columns = sorted(list(non_repeated_columns))

# Define the regex term for column validation, ignoring '0', 'NA', 'NSA', 'Unknown', and empty cells
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

# Load the CSV files and process columns separately
for file_name in os.listdir(directory_path):
    if file_name.endswith('.csv'):
        file_path = os.path.join(directory_path, file_name)
        df = pd.read_csv(file_path)

        # Dictionaries to store findings for the current file
        file_summary_repeated = {'file_name': file_name}
        file_summary_non_repeated = {'file_name': file_name}

        # Process repeated columns
        for column in repeated_columns:
            if column.lower() in ['offence', 'primary_offence']:
                # Apply special regex for OFFENCE/PRIMARY_OFFENCE (excluding 'Assault')
                count = count_valid_entries(df, column, regex_offence)
            else:
                # Apply general regex for all other columns
                count = count_valid_entries(df, column, regex_general)
            file_summary_repeated[column] = count

        # Process non-repeated columns
        for column in non_repeated_columns:
            if column.lower() in ['offence', 'primary_offence']:
                # Apply special regex for OFFENCE/PRIMARY_OFFENCE (excluding 'Assault')
                count = count_valid_entries(df, column, regex_offence)
            else:
                # Apply general regex for all other columns
                count = count_valid_entries(df, column, regex_general)
            file_summary_non_repeated[column] = count

        # Append the summary for repeated and non-repeated columns to their respective results lists
        results_repeated.append(file_summary_repeated)
        results_non_repeated.append(file_summary_non_repeated)

# Convert the list of dictionaries to DataFrames for repeated and non-repeated columns
results_df_repeated = pd.DataFrame(results_repeated)
results_df_non_repeated = pd.DataFrame(results_non_repeated)

# Write the results to separate CSV files
results_df_repeated.to_csv(output_repeated_file_path, index=False)
results_df_non_repeated.to_csv(output_non_repeated_file_path, index=False)

print(f"Summary reports saved to {output_repeated_file_path} and {output_non_repeated_file_path}")
