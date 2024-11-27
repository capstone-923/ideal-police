import pandas as pd
import numpy as np
from typing import List
from tqdm import tqdm


def fill_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fills missing values in a DataFrame column by averaging the previous and next cell values.
    If multiple consecutive cells are missing, fills them sequentially using interpolation.
    Ensures that the columns retain their original data types after filling.

    Args:
        df (pd.DataFrame): DataFrame with missing values.

    Returns:
        pd.DataFrame: DataFrame with missing values filled.
    """
    df = df.copy()
    original_dtypes = df.dtypes  # Store original data types

    for col in df.columns:
        if df[col].dtype in ['float64', 'int64']:  # Apply only for numeric columns
            # Fill missing values using linear interpolation
            df[col] = df[col].interpolate(method='linear', limit_direction='both')
        elif df[col].dtype == 'object':  # For string/object columns
            # Fill missing values with forward fill and backward fill
            df[col] = df[col].fillna(method='ffill').fillna(method='bfill')

    # Cast columns back to their original data types
    for col in df.columns:
        df[col] = df[col].astype(original_dtypes[col])

    return df


def expand_and_insert_neighborhoods(df: pd.DataFrame, area_mapping: pd.DataFrame) -> pd.DataFrame:
    """
    Expands the weather data DataFrame for all neighborhoods efficiently.
    Repeats each weather data row for all neighborhoods and inserts 'Neighborhood' and 'Neighborhood ID'
    directly after the 'Day' column.

    Args:
        df (pd.DataFrame): Weather data DataFrame.
        area_mapping (pd.DataFrame): Mapping of Area Code to Neighborhood.

    Returns:
        pd.DataFrame: Expanded DataFrame with neighborhood information added.
    """
    # Drop existing 'Neighborhood' and 'Neighborhood ID' columns if they exist
    df = df.drop(columns=["Neighborhood", "Neighborhood ID"], errors="ignore")

    num_neighborhoods = len(area_mapping)

    # Repeat each row of the weather data for all neighborhoods
    expanded_df = df.loc[df.index.repeat(num_neighborhoods)].reset_index(drop=True)

    # Create 'Neighborhood' and 'Neighborhood ID' data
    neighborhood_data = np.tile(area_mapping["Area Name"].values, len(df))
    neighborhood_id_data = np.tile(area_mapping["Area Code"].values, len(df))

    # Find the index after the 'Day' column
    day_index = expanded_df.columns.get_loc("Day") + 1

    # Insert 'Neighborhood' and 'Neighborhood ID' directly after 'Day'
    expanded_df.insert(day_index, "Neighborhood", neighborhood_data)
    expanded_df.insert(day_index + 1, "Neighborhood ID", neighborhood_id_data)

    return expanded_df


if __name__ == "__main__":
    # List of CSV paths for weather data
    csv_paths = [
        r"./Historical Climate Data/TORONTO_CITY/Cleaned/deep_clean_data.csv",
        r"./Historical Climate Data/TORONTO_CITY_CENTRE/Cleaned/deep_clean_data.csv",
        r"./Historical Climate Data/TORONTO_INTL_A/Cleaned/deep_clean_data.csv",
        r"./Historical Climate Data/TORONTO_NORTH_YORK/Cleaned/deep_clean_data.csv"
    ]

    # Path to the area mapping CSV (image 2 data)
    area_mapping_path = r"./toronto_neighborhood.csv"

    # Load the area mapping DataFrame
    area_mapping = pd.read_csv(area_mapping_path)

    # Process each CSV file
    for csv_path in csv_paths:
        print(f"Processing: {csv_path}")
        
        # Load the weather data DataFrame
        weather_df = pd.read_csv(csv_path)

        # Fill missing values
        weather_df = fill_missing_values(weather_df)
        output_path = csv_path.replace("deep_clean_data.csv", "filled_deep_clean_data.csv")
        weather_df.to_csv(output_path, index=False)
        print(f"Filled version is saved at: {output_path}")

        # Insert 'Neighborhood' and 'Neighborhood ID' columns and expand rows
        expanded_weather_df = expand_and_insert_neighborhoods(weather_df, area_mapping)
        output_path = csv_path.replace("deep_clean_data.csv", "processed_data.csv")
        expanded_weather_df.to_csv(output_path, index=False)
        print(f"Expanded version is saved at: {output_path}")
