# Scripts & Processed Climate Data

This repository contains scripts for downloading, processing, and analyzing Toronto's climate data. Most of data files can be found in the [Google Drive folder](https://drive.google.com/drive/folders/1lfvB6YeRG97RSXVScmtrVVjSsAthf6oX?usp=drive_link).

---

## Folder Overview

### **1. `climate_data`**

#### **`download_weather_data.sh`**:
- A shell script for downloading historical raw climate data from Environment Canada.
- Requires a `Cygwin` environment or Linux shell for execution.
- Downloads raw data for the following climate stations:
  - **TORONTO_CITY**
  - **TORONTO_CITY_CENTRE**
  - **TORONTO_INTL_A**
  - **TORONTO_NORTH_YORK**

  > **_Note_**: Dataset Details
  > - **Date Range**: 2014-01-01 to 2024-12-31  
  > - **Last Update**: Latest updates as of **2024-11-17** or **2024-11-24** (varies by station). Data beyond these dates is not available.
  > - **Original Datasets**: Access raw data and metadata in [Historical Climate Data](https://drive.google.com/drive/folders/1gMpm_jdO8CvqzOAeAdXA091jbS1Rt8dc?usp=drive_link).

#### **Cache.zip**
This archive, available on Google Drive, contains **mid-processed data** for all stations. Download it via [Cache.zip](https://drive.google.com/file/d/1dz3ONblQAtrLUcd2wokm4bT21gPzGfSJ/view?usp=drive_link).
Each station folder in `Cache.zip` contains the following intermediate files:

- **Merged Data**:
  - `merged_data.csv`: Consolidated raw data.
- **Cleaned Data**:
  - `basic_clean_data.csv`: Simplified dataset with unnecessary columns removed.
  - `basic_clean_data_report.csv`: Data quality analysis (Non-Blank Cell Rate) for `basic_clean_data.csv`.
  - `deep_clean_data.csv`: Data with selected features in a structured format.
  - `filled_deep_clean_data.csv`: Data with missing values filled via interpolation.

#### **processed_data.zip**
[processed_data.zip](https://drive.google.com/file/d/1iDcF_ue2426kqFgCm7rr8Y8puqZFQ7q0/view?usp=drive_link).
- **`TORONTO_CITY_processed_data.csv`**
- **`TORONTO_CITY_CENTRE_processed_data.csv`**
- **`TORONTO_INTL_A_processed_data.csv`**
- **`TORONTO_NORTH_YORK_processed_data.csv`**

#### **`PCC_matrix.csv`**
Contains the PCC matrix for the 4 climate stations.

---

### **2. `data_processing_script`**
This folder contains Python scripts for processing the downloaded climate data.

#### **`cat.py`**
- Concatenates historical climate data files for a specific station into a single `merged_data.csv`.

#### **`basic_clean.py`**
- Cleans `merged_data.csv` by removing unnecessary columns and creates:
  - `basic_clean_data.csv`: Simplified dataset.
  - `basic_clean_data_report.csv`: Report on the Non-Blank Cell Rate for each column.
- Insights:
  - The **TORONTO_INTL_A** dataset has the highest data completion rate and is prioritized for analysis.
  - Other datasets are secondary options for filling gaps or further analysis.

##### **Columns Removed**
**Not Required for Analysis**:
- *Longitude (x)*
- *Latitude (y)*
- *Climate ID*
- *Date/Time*

**Unrelated to Crime Analysis**:
- *Dir of Max Gust (10s deg)*
- *Dir of Max Gust Flag*
- *Spd of Max Gust (km/h)*
- *Spd of Max Gust Flag*
- *Heat Deg Days (°C)*
- *Heat Deg Days Flag*
- *Cool Deg Days (°C)*
- *Cool Deg Days Flag*

#### **`deep_clean.py`**
- Extracts specified features from `basic_clean_data.csv` and organizes them into `deep_clean_data.csv`.

##### **Selected Features (in order):**
- *Year*
- *Month*
- *Day*
- *Max Temp (°C)*
- *Min Temp (°C)*
- *Mean Temp (°C)*
- *Total Rain (mm)*
- *Total Snow (cm)*
- *Total Precip (mm)*

#### **`processed_data.py`**
- Fills missing values in `deep_clean_data.csv` using linear interpolation and saves as `filled_deep_clean_data.csv`.
- Expands interpolated data across Toronto neighborhoods and outputs the final processed data to the `climate_data` folder.

#### **`compare_pcc.py`**
- Calculates the Pearson Correlation Coefficient (PCC) matrix for Toronto's climate stations.
- Saves the resulting matrix as `PCC_matrix.csv` in the `climate_data` folder.

---
