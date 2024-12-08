import os
import pandas as pd
from typing import List

# Define the constant list of header names to remove
HEADERS_TO_REMOVE: List[str] = ['Longitude (x)', 'Latitude (y)', 'Climate ID', "Date/Time", # Not needed
                                'Dir of Max Gust (10s deg)', 'Dir of Max Gust Flag', 'Spd of Max Gust (km/h)', 'Spd of Max Gust Flag', # Not related to crime rates
                                'Heat Deg Days (°C)', 'Heat Deg Days Flag', 'Cool Deg Days (°C)', 'Cool Deg Days Flag', # Not related to crime rates
                                ]

def remove_trailing_empty_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes rows from the bottom of the DataFrame until there are non-empty cells
    in columns other than the first four columns.
    
    Args:
        df (pd.DataFrame): The DataFrame to process.
    
    Returns:
        pd.DataFrame: The cleaned DataFrame with trailing empty rows removed.
    """
    for i in range(len(df) - 1, -1, -1):
        # Check if all columns except the first 4 are empty in this row
        if df.iloc[i, 4:].notna().any():
            # Keep this row and everything above it
            return df.iloc[:i + 1]
    return df  # Return original if all rows are empty beyond the first 4 columns

def generate_report(df: pd.DataFrame, report_file_path: str) -> None:
    """
    Generates a horizontal report of non-blank cell rates for each header and saves it.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.
        report_file_path (str): Path to save the report.
    """
    # Calculate non-blank cell count and rate for each column
    total_rows = len(df)
    report_data = {
        "Metric": ["Non-Blank Cell Count", "Non-Blank Cell Rate (%)"],
    }
    for col in df.columns:
        non_blank_count = df[col].count()
        non_blank_rate = (non_blank_count / total_rows * 100) if total_rows > 0 else 0
        report_data[col] = [non_blank_count, non_blank_rate]

    # Create the DataFrame and save it
    report_df = pd.DataFrame(report_data)
    report_df.to_csv(report_file_path, index=False)

def process_csv_files_in_merged_directory(directory: str) -> None:
    """
    Processes the 'merged_data.csv' file in each subdirectory's 'Merged' folder
    by removing specified headers, removing trailing empty rows, and saving to a 
    parallel 'Cleaned' folder with a horizontal report of non-blank cell rates.

    Args:
        directory (str): Path to the base directory containing subdirectories with 'Merged' folders.
    """
    for subdir in os.listdir(directory):
        subdir_path: str = os.path.join(directory, subdir)
        
        # Ensure the path is a directory and matches the naming convention
        if not os.path.isdir(subdir_path) or "TORONTO_" not in subdir_path:
            continue

        print(f"\n{subdir}:")
        
        # Check if the 'Merged' folder exists in this subdirectory
        merged_folder_path: str = os.path.join(subdir_path, "Merged")
        if not os.path.isdir(merged_folder_path):
            print(f"No 'Merged' folder found. Skipping...")
            continue

        # Define the path to the merged CSV file
        merged_file_path: str = os.path.join(merged_folder_path, "merged_data.csv")
        if not os.path.exists(merged_file_path):
            print(f"No 'merged_data.csv' file found. Skipping...")
            continue

        # Create the parallel 'Cleaned' folder path
        cleaned_folder_path: str = os.path.join(subdir_path, "Cleaned")
        os.makedirs(cleaned_folder_path, exist_ok=True)

        # Define the path to save the cleaned file and report
        cleaned_file_path: str = os.path.join(cleaned_folder_path, "basic_clean_data.csv")
        report_file_path: str = os.path.join(cleaned_folder_path, "basic_clean_data_report.csv")

        # Process the merged CSV file
        try:
            # Read the CSV file
            df = pd.read_csv(merged_file_path)
            
            # Identify headers that exist in the CSV and are in the removal list
            headers_to_drop: List[str] = [header for header in HEADERS_TO_REMOVE if header in df.columns]
            
            # Remove the headers if they exist
            if headers_to_drop:
                df = df.drop(columns=headers_to_drop)
                print(f"Removed headers: {headers_to_drop}")
            else:
                print(f"Removed headers: None")

            # Remove trailing rows where all columns except the first 4 are empty
            df = remove_trailing_empty_rows(df)

            # Save the cleaned DataFrame to the 'Cleaned' folder
            df.to_csv(cleaned_file_path, index=False)
            print(f"Saved cleaned file to: {cleaned_file_path}")
            
            # Generate the horizontal report
            generate_report(df, report_file_path)
            print(f"Generated non-blank cell rate report: {report_file_path}")
        
        except Exception as e:
            print(f"Error processing: {merged_file_path}. Error: {e}")

def main(base_dir: str) -> None:
    """
    Loops through all subdirectories in the base directory, finds 'Merged' folders,
    processes 'merged_data.csv' files to remove specified headers, remove trailing empty rows,
    saves cleaned files to 'Cleaned' folders, and generates reports.

    Args:
        base_dir (str): Path to the base directory containing subdirectories with 'Merged' folders.
    """
    process_csv_files_in_merged_directory(base_dir)

if __name__ == "__main__":
    # Set the base directory
    base_directory: str = "./Historical Climate Data"  # Replace with your base folder
    
    # Run the main function
    main(base_directory)
