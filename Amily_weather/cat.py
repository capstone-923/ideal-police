import os
import pandas as pd
from typing import List

def merge_csv_files_in_directory(directory: str) -> None:
    """
    Merges all CSV files in a given directory into a single file, sorted by modification time.
    Saves the merged file into the same directory.

    Args:
        directory (str): Path to the directory containing CSV files.
    """
    # Initialize an empty list to store each CSV file's data
    data_frames: List[pd.DataFrame] = []

    # Get a list of all CSV files in the directory, sorted by modification time
    files: List[str] = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.csv')]
    files.sort(key=os.path.getmtime)

    # Check if there are any CSV files
    if not files:
        print(f"No CSV files found in {directory}.")
        return

    # Loop through each file in sorted order and read it into a DataFrame
    for file_path in files:
        data_frames.append(pd.read_csv(file_path))

    # Concatenate all DataFrames in the list into a single DataFrame
    merged_df = pd.concat(data_frames, ignore_index=True)

    # Create a subfolder for saving the merged file
    output_dir = os.path.join(directory, "Merged")
    os.makedirs(output_dir, exist_ok=True)

    # Define the output file path
    output_file = os.path.join(output_dir, "merged_data.csv")
    
    # Save the concatenated data to the output file
    merged_df.to_csv(output_file, index=False)

    # Print confirmation message with file path and order
    print(f"All CSV files in {directory} have been concatenated into {output_file} in order of 'Date Modified'.")

def main(base_dir: str) -> None:
    """
    Loops through all subdirectories in the base directory and merges CSV files in each directory.
    Saves each merged CSV into a separate "Merged" subfolder within its respective directory.

    Args:
        base_dir (str): Path to the base directory containing subdirectories with CSV files.
    """
    for subdir in os.listdir(base_dir):
        subdir_path: str = os.path.join(base_dir, subdir)
        
        if os.path.isdir(subdir_path) and "TORONTO_" in subdir_path:  # Check if it's a directory of weather station data
            merge_csv_files_in_directory(subdir_path)

if __name__ == "__main__":
    # Set the base directory
    base_directory: str = "./Historical Climate Data"  # Replace with your base folder
    
    # Run the main function
    main(base_directory)