import csv
import sys
import os
from datetime import datetime, timedelta

def sort_fill_dates_remove_hour(input_file):
    """
    Sorts rows in the CSV file by the DATE column (handling Unix timestamps), removes the hour field,
    and fills in missing dates with empty rows. The final DATE format is mm/dd/yyyy.

    Args:
        input_file (str): Path to the input CSV file.
    """
    output_file = f"final_{os.path.basename(input_file)}"
    print(f"Processing file: {input_file}")

    with open(input_file, mode='r', encoding='utf-8') as infile, \
         open(output_file, mode='w', encoding='utf-8', newline='') as outfile:

        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames

        # Parse rows and convert DATE column
        rows = []
        for row in reader:
            date_value = row['DATE'].strip()
            try:
                # Check if the date is a Unix timestamp
                if date_value.isdigit():
                    date = datetime.utcfromtimestamp(int(date_value) / 1000)
                else:
                    date = datetime.strptime(date_value, '%m/%d/%Y')
                # Remove hour field (set to midnight)
                date = date.replace(hour=0, minute=0, second=0, microsecond=0)
            except ValueError:
                print(f"Skipping invalid date: {date_value}")
                continue
            row['DATE'] = date
            rows.append(row)

        # Sort rows by DATE column
        sorted_rows = sorted(rows, key=lambda row: row['DATE'])

        # Generate all dates in the range
        start_date = sorted_rows[0]['DATE']
        end_date = sorted_rows[-1]['DATE']
        all_dates = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

        # Create a mapping of dates to rows
        date_to_row = {row['DATE']: row for row in sorted_rows}

        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        # Write rows, filling in missing dates with empty rows
        for date in all_dates:
            if date in date_to_row:
                row = date_to_row[date]
                row['DATE'] = date.strftime('%m/%d/%Y')
                writer.writerow(row)
            else:
                empty_row = {field: '' for field in fieldnames}
                empty_row['DATE'] = date.strftime('%m/%d/%Y')
                writer.writerow(empty_row)

    print(f"Rows sorted by DATE column, hour field removed, and missing dates filled.")
    print(f"Output file created: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    sort_fill_dates_remove_hour(input_file)
