import pandas as pd
import os

# Directory and output file paths
directory_path = '/home/ghamr/Downloads/'  # Replace with your directory path
output_file_path = 'summary_report.csv'  # Path for the output CSV file

# List to collect results
results = []

# Load the CSV files
for file_name in os.listdir(directory_path):
    if file_name.endswith('.csv'):
        file_path = os.path.join(directory_path, file_name)
        df = pd.read_csv(file_path)

        # Dictionary to store findings for the current file
        file_summary = {
            'file_name': file_name,
            'non_empty_bike_make_count': 0,
            'non_empty_bike_model_count': 0,
            'offence_not_assault_count': 0,
            'occ_date_2000_or_later_count': 0,
            'report_date_2000_or_later_count': 0,
            'neighbourhood_140_not_nsa_count': 0,
            'long_wgs84_not_nsa_count': 0,
            'lat_wgs84_not_nsa_count': 0,
        }

        # Check if 'BIKE_MAKE' column exists
        if 'BIKE_MAKE' in df.columns:
            # Convert to string, strip whitespace, and convert to lowercase
            bike_make_series = df['BIKE_MAKE'].astype(str).str.strip().str.lower()
            # Exclude entries that are empty or 'na'
            valid_bike_make = bike_make_series[~bike_make_series.isin(['', 'na'])]
            # Count the number of valid entries
            non_empty_bike_make = valid_bike_make.count()
            file_summary['non_empty_bike_make_count'] = non_empty_bike_make

        # Check if 'BIKE_MODEL' column exists
        if 'BIKE_MODEL' in df.columns:
            # Convert to string, strip whitespace, and convert to lowercase
            bike_model_series = df['BIKE_MODEL'].astype(str).str.strip().str.lower()
            # Exclude entries that are empty or 'na'
            valid_bike_model = bike_model_series[~bike_model_series.isin(['', 'na'])]
            # Count the number of valid entries
            non_empty_bike_model = valid_bike_model.count()
            file_summary['non_empty_bike_model_count'] = non_empty_bike_model

        # Check if 'OFFENCE' column exists
        if 'OFFENCE' in df.columns:
            # Convert to string, strip whitespace, and convert to lowercase
            offence_series = df['OFFENCE'].astype(str).str.strip().str.lower()
            # Exclude entries that are empty or 'na'
            valid_offence = offence_series[~offence_series.isin(['', 'na'])]
            # Count entries where 'OFFENCE' is not 'assault'
            non_assault_entries = valid_offence[valid_offence != 'assault']
            file_summary['offence_not_assault_count'] = non_assault_entries.count()

        # Check if 'OCC_DATE' column exists
        if 'OCC_DATE' in df.columns:
            # Convert 'OCC_DATE' to datetime, handling errors
            df['OCC_DATE'] = pd.to_datetime(df['OCC_DATE'], errors='coerce')
            # Filter entries where 'OCC_DATE' is in the year 2000 or later
            entries_after_2000 = df[df['OCC_DATE'].dt.year >= 2000]
            file_summary['occ_date_2000_or_later_count'] = len(entries_after_2000)

        # Check if 'REPORT_DATE' column exists
        if 'REPORT_DATE' in df.columns:
            # Convert 'REPORT_DATE' to datetime, handling errors
            df['REPORT_DATE'] = pd.to_datetime(df['REPORT_DATE'], errors='coerce')
            # Filter entries where 'REPORT_DATE' is in the year 2000 or later
            report_entries_after_2000 = df[df['REPORT_DATE'].dt.year >= 2000]
            file_summary['report_date_2000_or_later_count'] = len(report_entries_after_2000)

        # Check if 'NEIGHBOURHOOD_140' column exists
        if 'NEIGHBOURHOOD_140' in df.columns:
            # Convert to string, strip whitespace, and convert to lowercase
            neighbourhood_series = df['NEIGHBOURHOOD_140'].astype(str).str.strip().str.lower()
            # Exclude entries that are empty, 'na', or 'nsa'
            valid_neighbourhood = neighbourhood_series[~neighbourhood_series.isin(['', 'na', 'nsa'])]
            # Count the number of valid entries
            neighbourhood_count = valid_neighbourhood.count()
            file_summary['neighbourhood_140_not_nsa_count'] = neighbourhood_count

        # Check if 'LONG_WGS84' column exists
        if 'LONG_WGS84' in df.columns:
            # Convert to string, strip whitespace, and convert to lowercase
            long_series = df['LONG_WGS84'].astype(str).str.strip().str.lower()
            # Exclude entries that are empty, 'na', or 'nsa'
            valid_long = long_series[~long_series.isin(['', 'na', 'nsa', '0'])]
            # Count the number of valid entries
            long_count = valid_long.count()
            file_summary['long_wgs84_not_nsa_count'] = long_count

        # Check if 'LAT_WGS84' column exists
        if 'LAT_WGS84' in df.columns:
            # Convert to string, strip whitespace, and convert to lowercase
            lat_series = df['LAT_WGS84'].astype(str).str.strip().str.lower()
            # Exclude entries that are empty, 'na', or 'nsa'
            valid_lat = lat_series[~lat_series.isin(['', 'na', 'nsa', '0'])]
            # Count the number of valid entries
            lat_count = valid_lat.count()
            file_summary['lat_wgs84_not_nsa_count'] = lat_count
        
        # Check if 'REPORT_HOUR' column exists
        if 'REPORT_HOUR' in df.columns:
            report_hour_series = df['REPORT_HOUR'].astype(str).str.strip().str.lower()
            valid_report_hour = report_hour_series[~report_hour_series.isin(['', 'na'])]
            report_hour_count = valid_report_hour.count()
            file_summary['report_hour_count'] = report_hour_count

        # Check if 'OCC_HOUR' column exists
        if 'OCC_HOUR' in df.columns:
            occ_hour_series = df['OCC_HOUR'].astype(str).str.strip().str.lower()
            valid_occ_hour = occ_hour_series[~occ_hour_series.isin(['', 'na'])]
            occ_hour_count = valid_occ_hour.count()
            file_summary['occ_hour_count'] = occ_hour_count
        if 'NEIGHBOURHOOD_158' in df.columns:
            neighbourhood_158_series = df['NEIGHBOURHOOD_158'].astype(str).str.strip().str.lower()
            valid_neighbourhood_158 = neighbourhood_158_series[~neighbourhood_158_series.isin(['', 'na', 'nsa'])]
            neighbourhood_158_count = valid_neighbourhood_158.count()
            file_summary['neighbourhood_158_not_nsa_count'] = neighbourhood_158_count
        # Append the summary for the current file to the results list
        results.append(file_summary)
        # Check if 'UCR_CODE' column exists
        if 'UCR_CODE' in df.columns:
            ucr_code_series = df['UCR_CODE'].astype(str).str.strip().str.lower()
            valid_ucr_code = ucr_code_series[~ucr_code_series.isin(['', 'na'])]
            ucr_code_count = valid_ucr_code.count()
            file_summary['ucr_code_count'] = ucr_code_count
        
        # Check if 'UCR_EXT' column exists
        if 'UCR_EXT' in df.columns:
            ucr_ext_series = df['UCR_EXT'].astype(str).str.strip().str.lower()
            valid_ucr_ext = ucr_ext_series[~ucr_ext_series.isin(['', 'na'])]
            ucr_ext_count = valid_ucr_ext.count()
            file_summary['ucr_ext_count'] = ucr_ext_count

# Convert the list of dictionaries to a DataFrame
results_df = pd.DataFrame(results)

# Write the results to a CSV file
results_df.to_csv(output_file_path, index=False)

print(f"Summary report saved to {output_file_path}")
