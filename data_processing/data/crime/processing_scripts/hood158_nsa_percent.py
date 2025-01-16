import csv
import sys
import os

def count_hood_158(input_file):
    """
    Counts the number of entries in the HOOD_158 column that are empty or have the value "NSA".

    Args:
        input_file (str): Path to the input CSV file.
    """

    total_rows = 0
    empty_or_nsa = 0

    with open(input_file, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)

        for row in reader:
            total_rows += 1
            hood_value = row.get('HOOD_158', '').strip()
            if not hood_value or hood_value.upper() == 'NSA':
                empty_or_nsa += 1

    # Print results
    print(f"Total rows processed: {total_rows}")
    print(f"Rows where HOOD_158 is empty or 'NSA' in {os.path.basename(input_file)}: {empty_or_nsa}")
    if total_rows > 0:
        print(f"Percentage: {empty_or_nsa / total_rows * 100:.2f}%")
        print()
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    count_hood_158(input_file)
