import csv
import sys

def filter_columns(column_list_file, input_file, output_file):
    """
    Reads a list of column names from a CSV file, compares them to the columns in another CSV file.
    Prints any missing column names, and outputs a file with only the matching columns.
    
    Args:
        column_list_file (str): Path to the CSV file containing the list of column names.
        input_file (str): Path to the input CSV file to filter.
        output_file (str): Path to the output CSV file with filtered columns.
    """

    # Read column names from the column list file (comma-separated list assumed)
    with open(column_list_file, mode='r', encoding='utf-8') as col_file:
        column_list = next(csv.reader(col_file))

    # Read input CSV and compare columns
    with open(input_file, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        input_columns = reader.fieldnames

        # Print missing columns
        missing_in_input = [col for col in column_list if col not in input_columns]
        if missing_in_input:
            print("===============================")
            print(f"Input file: {input_file}")
            print("Columns in the list but missing in the input file:", ", ".join(missing_in_input))
            print("===============================")

        # missing_in_list = [col for col in input_columns if col not in column_list]
        # if missing_in_list:
        #     print("Columns in the input file but missing in the list:", ", ".join(missing_in_list))

        # Filter columns to include only those in the column list
        matching_columns = [col for col in column_list if col in input_columns]

        # Write output file with only the matching columns
        with open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=matching_columns)
            writer.writeheader()
            for row in reader:
                writer.writerow({col: row[col] for col in matching_columns})

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <column_list_file> <input_file> <output_file>")
        sys.exit(1)

    column_list_file = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    filter_columns(column_list_file, input_file, output_file)
    
