import csv
import sys
import os
import re

def consolidate_dates(input_file):
    """
    Consolidates OCC_DATE and REPORT_DATE into a single DATE column.
    Uses OCC_DATE if available; otherwise, uses REPORT_DATE.
    Removes the time portion "5:00:00 AM" from dates if it exists.
    Prints statistics on missing or mismatched dates.

    Args:
        input_file (str): Path to the input CSV file.
    """
    output_file = f"consolidated_{os.path.basename(input_file)}"

    total_rows = 0
    missing_both = 0
    report_only = 0
    occurrence_only = 0

    with open(input_file, mode='r', encoding='utf-8') as infile, \
         open(output_file, mode='w', encoding='utf-8', newline='') as outfile:

        reader = csv.DictReader(infile)
        fieldnames = ['DATE'] + [col for col in reader.fieldnames if col not in ('OCC_DATE', 'REPORT_DATE')]

        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            total_rows += 1
            occ_date = row.get('OCC_DATE', '').strip()
            report_date = row.get('REPORT_DATE', '').strip()

            if not occ_date and not report_date:
                missing_both += 1
            elif not occ_date and report_date:
                report_only += 1
            elif occ_date and not report_date:
                occurrence_only += 1

            # Consolidate dates
            date = occ_date if occ_date else report_date
            date = re.sub(r'\s*5:00:00 AM$', '', date)  # Remove time portion if it exists
            new_row = {'DATE': date}
            new_row.update({col: row[col] for col in reader.fieldnames if col not in ('OCC_DATE', 'REPORT_DATE')})
            writer.writerow(new_row)

    # Calculate percentages
    if total_rows > 0:
        print(f"Percentage of rows missing both OCC_DATE and REPORT_DATE: {missing_both / total_rows * 100:.2f}%")
        print(f"Percentage of rows with REPORT_DATE but no OCC_DATE: {report_only / total_rows * 100:.2f}%")
        print(f"Percentage of rows with OCC_DATE but no REPORT_DATE: {occurrence_only / total_rows * 100:.2f}%")

    print(f"Output file created: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    consolidate_dates(input_file)
