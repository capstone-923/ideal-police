import pandas as pd
import glob

# Step 1: Get list of CSV files
file_list = glob.glob('/home/ghamr/Downloads/*.csv')  # Update the path accordingly

# Step 2: Collect columns from each file
file_columns_map = {}
for file in file_list:
    df = pd.read_csv(file)
    columns_set = frozenset(df.columns)
    file_columns_map[file] = columns_set

# Step 3: Group files by their columns sets
columns_files_map = {}
for file, columns_set in file_columns_map.items():
    columns_files_map.setdefault(columns_set, []).append(file)

# Step 4: Display all files and their columns
for columns_set, files in columns_files_map.items():
    if len(files) > 1:
        print(f"The following files have the same columns:")
        for f in files:
            print(f" - {f}")
    else:
        print(f"The following file has unique columns:")
        print(f" - {files[0]}")
    print(f"Columns: {sorted(columns_set)}")
    print('---')
    print("number of files: ", len(files))
    print("number of columns: ", len(columns_set))