#3
import os
import pandas as pd

input_csv_path = "/content/test_ground" #the path pointing toward the FOLDER containing all CSV files
output_csv_path = "/content/cont1.csv" #outputs the concatenated CSV file
def concatenate_csv_files(input_directory: str, output_file: str) -> None:
    """
    Concatenates all CSV files in the specified directory into a single CSV file.

    Arguments:
    input_directory: str
        The path to the directory containing the CSV files to be concatenated.
    output_file: str
        The path (including the file name) where the combined CSV file will be saved.

    Functionality:
    - Iterates through all files in the provided directory.
    - Checks if each file has a `.csv` extension and is a valid file.
    - Reads the content of valid CSV files into Pandas DataFrames.
    - Concatenates all the DataFrames into a single DataFrame.
    - Saves the resulting DataFrame as a new CSV file at the specified output path.

    Returns:
    None
    """

    # List to hold dataframes
    dataframes = []

    # Loop through all files in the directory
    for file_name in os.listdir(input_directory):
        file_path = os.path.join(input_directory, file_name)

        # Check if the file is a CSV
        if os.path.isfile(file_path) and file_name.endswith('.csv'):
            print(f"Processing file: {file_name}")
            try:
                # Read the CSV file into a dataframe
                df = pd.read_csv(file_path)
                dataframes.append(df)
            except Exception as e:
                print(f"Error reading {file_name}: {e}")

    # Concatenate all dataframes
    if dataframes:
        combined_df = pd.concat(dataframes, ignore_index=True)
        # Save the combined dataframe to a new CSV file
        combined_df.to_csv(output_file, index=False)
        print(f"Combined CSV saved to: {output_file}")
    else:
        print("No CSV files found in the directory.")

def main():
    concatenate_csv_files(input_csv_path,output_csv_path)


if __name__ == "__main__":
    main()