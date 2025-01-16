import csv
import sys
import os
from datetime import datetime, timedelta

def sort_and_fill_dates(input_file):
    """
    Sorts rows in the CSV file by the DATE column and fills in missing dates with empty rows.
    Assumes the DATE column is in the format month/day/year (e.g., 1/3/2004).

    Args:
        input_file (str): Path to the input CSV file.
    """
    output_file = f"sorted_filled_{os.path.basename(input_file)}"
    print(f"Processing file: {input_file}")

    with open(input_file, mode='r', encoding='utf-8') as infile, \
         open(output_file, mode='w', encoding='utf-8', newline='') as outfile:

        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames

        # Parse rows and sort by DATE
        rows = list(reader)
        sorted_rows = sorted(rows, key=lambda row: datetime.strptime(row['DATE'], '%m/%d/%Y'))

        # Generate all dates in the range
        start_date = datetime.strptime(sorted_rows[0]['DATE'], '%m/%d/%Y')
        end_date = datetime.strptime(sorted_rows[-1]['DATE'], '%m/%d/%Y')
        all_dates = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

        # Create a mapping of dates to rows
        date_to_row = {datetime.strptime(row['DATE'], '%m/%d/%Y'): row for row in sorted_rows}

        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        # Write rows, filling in missing dates with empty rows
        for date in all_dates:
            date_str = date.strftime('%m/%d/%Y')
            if date in date_to_row:
                writer.writerow(date_to_row[date])
            else:
                empty_row = {field: '' for field in fieldnames}
                empty_row['DATE'] = date_str
                writer.writerow(empty_row)

    print(f"Rows sorted by DATE column and missing dates filled with empty rows.")
    print(f"Output file created: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    sort_and_fill_dates(input_file)
