import pandas as pd

# Load the Excel file
file_path = './neighbourhood-profiles-2021-158-model.xlsx'  # Replace with the path to your Excel file
excel_data = pd.ExcelFile(file_path)

# Load the 'Nbhdmetadata' sheet
sheet_metadata = pd.read_excel(file_path, sheet_name='Nbhdmetadata')

# Extract neighborhood name and neighborhood number
neighborhood_data = sheet_metadata[['HDNUM', 'HDNAME']].copy()  # Explicitly make a copy
neighborhood_data.rename(columns={'HDNUM': 'Neighborhood Number', 'HDNAME': 'Neighborhood Name'}, inplace=True)

# Save the extracted data to a CSV file
output_path = 'neighborhood_data.csv'  # Replace with the desired output path
neighborhood_data.to_csv(output_path, index=False)

print(f"Data has been saved to {output_path}")
