# Scripts & Processed Climate Data

This repository contains scripts and processed data related to Toronto's climate stations. Processed data is stored in the `Climate Data` folder. For detailed information about the data, refer to the `README.md` file in that folder.

---

## Climate Data Folder Overview

Four Toronto climate stations are selected for analysis:
- **TORONTO_CITY**
- **TORONTO_CITY_CENTRE**
- **TORONTO_INTL_A**
- **TORONTO_NORTH_YORK**

---

## Scripts Overview

### **1. cat.py**
- Concatenates historical climate data CSV files for a single station into a unified file: `merged_data.csv`.

---

### **2. basic_clean.py**
- Cleans `merged_data.csv` by removing irrelevant header columns and saves the result as `basic_clean_data.csv`.
- Generates a report on the **Non-Blank Cell Rate** for each column in `basic_clean_data.csv`:
  - The report is saved as `basic_clean_data_report.csv`.
  - The report provides insights into data quality across the four stations:
    - The `TORONTO_INTL_A` dataset is prioritized due to its high data completion rate.
    - Other datasets are treated as secondary options (Plan B) for filling in gaps or additional analysis.

#### Columns Removed:
**Unneeded for Analysis**:
- `Longitude (x)`
- `Latitude (y)`
- `Climate ID`
- `Date/Time`

**Not Related to Crime Rates**:
- `Dir of Max Gust (10s deg)`
- `Dir of Max Gust Flag`
- `Spd of Max Gust (km/h)`
- `Spd of Max Gust Flag`
- `Heat Deg Days (°C)`
- `Heat Deg Days Flag`
- `Cool Deg Days (°C)`
- `Cool Deg Days Flag`

---

### **3. deep_clean.py**
- Extracts only the selected features from `basic_clean_data.csv`, organizes them in a specified order, and saves the result as `deep_clean_data.csv`.

#### Selected Features and Order:
The extracted features are specified in the following order:
- `Year`
- `Month`
- `Day`
- `Data`
- `Quality`
- `Max Temp (°C)`
- `Min Temp (°C)`
- `Mean Temp (°C)`
- `Total Rain (mm)`
- `Total Snow (cm)`
- `Total Precip (mm)`

---

### **4. extract_neighbourhood.py**
- Reads a GeoJSON file (`toronto_crs84.geojson`) to extract Toronto neighbourhood information.
- Saves the extracted data to `toronto_neighbourhood.csv`.

#### Output Headers:
The extracted data includes the following headers:
- `Area Code`
- `Area Name`
- `Geometry Type`
- `Coordinates`

---

### **5. process_data.py**
- Fills blank values in `deep_clean_data.csv` using linear interpolation (average of previous and next values).
- Saves the result as `filled_deep_clean_data.csv`.
- Expands the interpolated data based on Toronto neighbourhoods.
- Saves the final expanded data to `processed_data.csv`.

#### Example Input and Output of Data Expansion According to neighbourhood:

**Input Weather Data (`df`):**
| Year | Month | Day | Max Temp (°C) | Min Temp (°C) |
|------|-------|-----|---------------|---------------|
| 2014 | 1     | 1   | -8.4          | -14.5         |
| 2014 | 1     | 2   | -5.0          | -10.0         |

**Area Mapping (`area_mapping`):**
| Area Code | Area Name            |
|-----------|----------------------|
| 97        | Yonge-St.Clair       |
| 123       | Yorkdale-Glen Park   |

**Expanded DataFrame:**
| Year | Month | Day | neighbourhood         | neighbourhood ID | Max Temp (°C) | Min Temp (°C) |
|------|-------|-----|----------------------|-----------------|---------------|---------------|
| 2014 | 1     | 1   | Yonge-St.Clair       | 97              | -8.4          | -14.5         |
| 2014 | 1     | 1   | Yorkdale-Glen Park   | 123             | -8.4          | -14.5         |
| 2014 | 1     | 2   | Yonge-St.Clair       | 97              | -5.0          | -10.0         |
| 2014 | 1     | 2   | Yorkdale-Glen Park   | 123             | -5.0          | -10.0         |
> **_Note:_** Same weather condition is applied to all toronto unit zones.
---

### **6. compare_pcc.py**
- Computes the Pearson Correlation Coefficient (PCC) matrix for all Toronto climate stations.
- Saves the correlation matrix as `PCC_matrix.csv`.

#### Example PCC Matrix:

|                      | TORONTO_CITY | TORONTO_CITY_CENTRE | TORONTO_INTL_A | TORONTO_NORTH_YORK |
|----------------------|--------------|----------------------|----------------|--------------------|
| **TORONTO_CITY**     | 1.0          | 0.85                 | 0.78           | 0.81               |
| **TORONTO_CITY_CENTRE** | 0.85       | 1.0                  | 0.82           | 0.87               |
| **TORONTO_INTL_A**   | 0.78         | 0.82                 | 1.0            | 0.76               |
| **TORONTO_NORTH_YORK** | 0.81       | 0.87                 | 0.76           | 1.0                |
