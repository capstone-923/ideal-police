import pandas as pd
import numpy as np
from typing import Dict


def calculate_pcc_matrix(station_data: Dict[str, str], output_path: str) -> None:
    """
    Calculates the Pearson Correlation Coefficient (PCC) matrix between weather data from multiple stations.
    Only compares numeric columns, excluding 'Year', 'Month', and 'Day'.
    Removes columns if one of the stations in the pair has it completely empty.

    Args:
        station_data (Dict[str, str]): Dictionary where keys are station names and values are file paths.
        output_path (str): Path to save the PCC matrix as a CSV file.

    Returns:
        None
    """
    # Load data from each station into a dictionary of DataFrames
    station_dfs = {}
    for station_name, station_file in station_data.items():
        df = pd.read_csv(station_file)

        # Drop non-numeric columns (e.g., Year, Month, Day)
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        df = df[numeric_columns]

        # Drop columns that are entirely empty
        df = df.dropna(axis=1, how="all")

        # Store the DataFrame
        station_dfs[station_name] = df

    # Align dataframes to the shortest length
    min_length = min(len(df) for df in station_dfs.values())
    for station in station_dfs:
        station_dfs[station] = station_dfs[station].iloc[:min_length]

    # Create a correlation matrix DataFrame
    station_names = list(station_dfs.keys())
    pcc_matrix = pd.DataFrame(index=station_names, columns=station_names, dtype=float)

    # Calculate PCC between each pair of stations column by column
    for station1, df1 in station_dfs.items():
        for station2, df2 in station_dfs.items():
            if station1 == station2:
                pcc_matrix.loc[station1, station2] = 1.0  # Correlation of a station with itself is 1
            else:
                # Align columns and drop ones that are entirely empty in either DataFrame
                common_columns = df1.columns.intersection(df2.columns)
                df1_filtered = df1[common_columns]
                df2_filtered = df2[common_columns]

                # Remove columns that are completely empty in either DataFrame
                valid_columns = [col for col in common_columns if not (df1_filtered[col].isna().all() or df2_filtered[col].isna().all())]
                if valid_columns:
                    combined_corr = [
                        df1_filtered[col].corr(df2_filtered[col], method="pearson")
                        for col in valid_columns
                    ]
                    avg_pcc = np.mean(combined_corr)
                    pcc_matrix.loc[station1, station2] = avg_pcc
                else:
                    pcc_matrix.loc[station1, station2] = np.nan  # No valid columns for comparison

    # Save the PCC matrix to a CSV file without an extra index label
    pcc_matrix.to_csv(output_path, index_label=None)
    print(f"PCC matrix saved to: {output_path}")


if __name__ == "__main__":
    # Dictionary of station names and file paths
    station_data = {
        "TORONTO_CITY": "./Historical Climate Data/TORONTO_CITY/Cleaned/deep_clean_data.csv",
        "TORONTO_CITY_CENTRE": "./Historical Climate Data/TORONTO_CITY_CENTRE/Cleaned/deep_clean_data.csv",
        "TORONTO_INTL_A": "./Historical Climate Data/TORONTO_INTL_A/Cleaned/deep_clean_data.csv",
        "TORONTO_NORTH_YORK": "./Historical Climate Data/TORONTO_NORTH_YORK/Cleaned/deep_clean_data.csv"
    }

    # Output path for PCC matrix
    output_path = "./Historical Climate Data/PCC_matrix.csv"

    # Calculate and save the PCC matrix
    calculate_pcc_matrix(station_data, output_path)
