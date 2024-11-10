#!/usr/bin/env python3
import pandas as pd
import os
import re

input_files = "/home/ghamr/Downloads/"
output_folder = "/home/ghamr/Desktop/ECE496/data_analysis_initial/cleaned_files"

def clean_csv_files_in_directory(input_directory, output_folder):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Define regex pattern for case-insensitive matching of 'NA', 'NSA', 'NAN'
    missing_values_pattern = re.compile(r"^(na|nsa|nan)$", re.IGNORECASE)

    # Iterate through all CSV files in the input directory
    for file_name in os.listdir(input_directory):
        if file_name.endswith(".csv"):
            input_file = os.path.join(input_directory, file_name)
            try:
                # Load the CSV file
                df = pd.read_csv(input_file)

                # Apply a function to each cell to mark rows with 'NA', 'NSA', 'NAN' for removal
                def check_missing_values(cell):
                    if isinstance(cell, str):
                        return bool(missing_values_pattern.match(cell.strip()))
                    return False

                # Remove rows that contain any of the matching missing values
                df_cleaned = df[~df.map(check_missing_values).any(axis=1)]

                # Define the output file path
                output_file = os.path.join(output_folder, file_name)

                # Save the cleaned DataFrame to a new CSV file
                df_cleaned.to_csv(output_file, index=False)
                print(f"Cleaned file saved as: {output_file}")
            
            except Exception as e:
                print(f"Error processing {input_file}: {e}")


clean_csv_files_in_directory(input_files, output_folder)
