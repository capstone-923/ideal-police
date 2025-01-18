# Scripts & Processed Climate Data

This folder contains scripts for downloading, processing and anlayizing Crime data in Toronto. All data files except the raw, unprocessed files can be found in [this Google Drive folder](https://drive.google.com/drive/folders/1aqqX_oU9NU3krBmTy2BCVC6_l2n9GGAX)

The there are 2 final sets of data that include [hourly](https://drive.google.com/drive/folders/1cKoVqwKWtD73GGWgbUac_kZPn-OvSHRc) and [daily](https://drive.google.com/drive/folders/1Pj2EWwnNRkIZQp1DoZ6zjI4eWhHpGLvs) formats. The difference is that the former has a column for the hour of the crime occurrance

The datasets that are analyzed in this directory are the following:
-  [**Shooting and Firearm Discharges Open Data**](https://data.torontopolice.on.ca/datasets/64ddeca12da34403869968ec725e23c4_0/explore)
-  [**Homicides Open Data**](https://data.torontopolice.on.ca/datasets/d96bf5b67c1c49879f354dad51cf81f9_0/explore?location=43.722928%2C-79.374074%2C10.57)
-  [**Assault Open Data**](https://data.torontopolice.on.ca/datasets/b4d0398d37eb4aa184065ed625ddb922_0/explore?location=18.083507%2C-39.819624%2C3.11)
-  [**Auto Theft Open Data**](https://data.torontopolice.on.ca/datasets/95ab41aee16847dba8453bf1688249d6_0/explore?location=18.083507%2C-39.819624%2C3.11)
-  [**Bicycle Thefts Open Data**](https://data.torontopolice.on.ca/datasets/a89d10d5e28444ceb0c8d1d4c0ee39cc_0/explore?location=18.079128%2C-39.811113%2C3.11)
-  [**Break and Enter Open Data**](https://data.torontopolice.on.ca/datasets/040ead448df2412da252cfbb532e77ac_0/explore?location=18.079869%2C-39.818263%2C3.11)
-  [**Robbery Open Data**](https://data.torontopolice.on.ca/datasets/d0e1e98de5f945faa2fe635dee3f4062_0/explore?location=18.080583%2C-39.813030%2C3.11)
-  [**Theft Over Open Data**](https://data.torontopolice.on.ca/datasets/7530d9b637c340059ccb81a782481c04_0/explore?location=18.080995%2C-39.818263%2C3.11)
-  [**Theft From Motor Vehicle Open Data**](https://data.torontopolice.on.ca/datasets/d9303bc20f8a4351b7744a8703eecb80_0/explore?location=18.083507%2C-39.819624%2C3.11)
-  [**Hate Crimes Open Data**](https://data.torontopolice.on.ca/datasets/3dc9a8fae28b42c7aaf8fc62c7fbfdaa_0/explore)
-  [**Traffic Collisions Open Data (ASR-T-TBL-001)**](https://data.torontopolice.on.ca/datasets/bc4c72a793014a55a674984ef175a6f3_0/explore?location=18.083507%2C-39.819624%2C3.11)

---
## Overview of This Directory

- The [download_datasets.py](https://github.com/capstone-923/ideal-police/blob/crime_data/data_processing/data/crime/download_datasets.py) python file downloads all 11 datasets that were considered for this analysis automatically from the [Toronto Police Service Public Safety Data Portal](https://data.torontopolice.on.ca/)
  - This script requires the python regex library to be installed: pip install regex / pip3 install regex
- The [processing_scripts](https://github.com/capstone-923/ideal-police/tree/crime_data/data_processing/data/crime/processing_scripts) sub directory incldues all processing scripts used for intermediate processing of the data
> **_Note_**:  Dataset details
> - all files have OCC_DATE/OCCURANCE_DATE column
> - all files except Homicides have an occ_hour
> - I don't believe there is any need for interpolation since the empty cells do not have any crime
> - Since the crimes related to traffic collisions are all in th Traffic_Collisions dataset, other datasets that individualize them were not considered. This is especially because others do not include those without a death incident 
