import pandas as pd
import os
from typing import List

def process_csv(
    csv_path: str, 
    wanted_headers: List[str]
) -> pd.DataFrame:
    """
    Reads a CSV file and keeps only the specified headers and headers containing specified keywords.

    Args:
        csv_path (str): Path to the CSV file.
        wanted_headers (List[str]): List of exact header names to keep.
        keywords_to_include (List[str]): List of keywords; headers containing these will also be kept.

    Returns:
        pd.DataFrame: Processed DataFrame with only the desired columns.
    """
    try:
        # Read the CSV file
        df: pd.DataFrame = pd.read_csv(csv_path)

        # Determine the columns to keep
        columns_to_keep = [
            col for col in df.columns 
            if col in wanted_headers
        ]

        # Return the filtered DataFrame
        return df[columns_to_keep]
    except Exception as e:
        print(f"Error processing file {csv_path}: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error


if __name__ == "__main__":
    # List of CSV file paths
    csv_paths: List[str] = [
        r".\Historical Climate Data\TORONTO_CITY\Cleaned\basic_clean_data.csv",
        r".\Historical Climate Data\TORONTO_CITY_CENTRE\Cleaned\basic_clean_data.csv",
        r".\Historical Climate Data\TORONTO_INTL_A\Cleaned\basic_clean_data.csv",
        r".\Historical Climate Data\TORONTO_NORTH_YORK\Cleaned\basic_clean_data.csv"
    ]
    save_name = "deep_clean_data.csv"

    # Headers to keep (exact match)
    wanted_headers: List[str] = ["Year", "Month", "Day", "Data", "Quality", "Max Temp (°C)", "Min Temp (°C)", "Mean Temp (°C)", "Total Rain (mm)", "Total Snow (cm)", "Total Precip (mm)"]

    # Process and save each CSV file
    for csv_path in csv_paths:
        # Process the CSV file
        processed_df = process_csv(csv_path, wanted_headers)

        # Save the processed DataFrame
        if not processed_df.empty:
            output_path = csv_path.replace("basic_clean_data.csv", save_name)
            processed_df.to_csv(output_path, index=False)
