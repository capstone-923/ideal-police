import csv
import sys
import os

def remove_nsa_or_empty(input_file):
    """
    Removes rows where the HOOD_158 column is empty or has the value "NSA".

    Args:
        input_file (str): Path to the input CSV file.
    """
    output_file = f"nsa_hood158_removed_{os.path.basename(input_file)}"
    print(f"Processing file: {input_file}")

    total_rows = 0
    removed_rows = 0

    with open(input_file, mode='r', encoding='utf-8') as infile, \
         open(output_file, mode='w', encoding='utf-8', newline='') as outfile:

        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)

        writer.writeheader()

        for row in reader:
            total_rows += 1
            hood_value = row.get('HOOD_158', '').strip()
            if not hood_value or hood_value.upper() == 'NSA':
                removed_rows += 1
                continue
            writer.writerow(row)

    print(f"Total rows processed: {total_rows}")
    print(f"Rows removed (empty or 'NSA' in HOOD_158): {removed_rows}")
    print(f"Filtered file created: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    remove_nsa_or_empty(input_file)
