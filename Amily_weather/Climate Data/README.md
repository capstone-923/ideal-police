# Climate Data

## Dataset Information

- **Dataset Range**: 2014-01-01 to 2024-12-31  
- **Update Status**: Latest data updates are as of **2024-11-17** or **2024-11-24**, depending on the station. Data for subsequent periods is currently unavailable.
- **Original Datasets**: Access the source datasets and metadata via this [Google Drive link](https://drive.google.com/drive/folders/1aQ57kK6zH4uhUdYq4fco-yBhqDeTyKWw?usp=drive_link).

---

## Folder Structure and Contents

### **1. Climate Stations**
This folder contains data from **all Toronto weather stations** with **daily** records available from **2014 to the most recent updates (2024)**. Four key stations are highlighted:
- **TORONTO_CITY**
- **TORONTO_CITY_CENTRE**
- **TORONTO_INTL_A**
- **TORONTO_NORTH_YORK**

Each station folder includes the following subfolders:
- **Merged**: 
  - `merged_data.csv`
- **Cleaned**: Contains processed data files:
  - `basic_clean_data.csv`: Columns with unnecessary features removed.
  - `basic_clean_data_report.csv`: Non-Blank Cell Rate analysis for `basic_clean_data.csv`.
  - `deep_clean_data.csv`: Includes selected features in a formatted order.
  - `filled_deep_clean_data.csv`: Missing values filled via linear interpolation.
  - `processed_data.csv`: Weather data expanded based on Toronto neighborhoods.

### **2. Script**
- `download_weather_data.sh`: A shell script for downloading data for the four climate stations via Cygwin.

### **3. Correlation Analysis**
- `PCC_matrix.csv`: Pearson correlation coefficient matrix for the four climate stations.

---

## Stations Table

| Station              | Climate ID | Station ID | Data Link                                                                                     |
|----------------------|------------|------------|---------------------------------------------------------------------------------------------|
| TORONTO CITY         | 6158355    | 31688      | [View Data](https://climate.weather.gc.ca/climate_data/daily_data_e.html?hlyRange=2002-06-04%7C2024-11-23&dlyRange=2002-06-04%7C2024-11-23&mlyRange=2003-07-01%7C2006-12-01&StationID=31688&Prov=ON&timeframe=2) |
| TORONTO CITY CENTRE  | 6158359    | 48549      | [View Data](https://climate.weather.gc.ca/climate_data/daily_data_e.html?hlyRange=2009-12-10%7C2024-11-23&dlyRange=2010-02-02%7C2024-11-23&mlyRange=%7C&StationID=48549&Prov=ON&timeframe=2) |
| TORONTO NORTH YORK   | 615S001    | 26953      | [View Data](https://climate.weather.gc.ca/climate_data/daily_data_e.html?hlyRange=%7C&dlyRange=1994-11-01%7C2024-11-17&mlyRange=1994-01-01%7C2006-12-01&StationID=26953&Prov=ON&timeframe=2) |
| TORONTO INTL A       | 6158731    | 51459      | [View Data](https://climate.weather.gc.ca/climate_data/daily_data_e.html?hlyRange=2013-06-11%7C2024-11-23&dlyRange=2013-06-13%7C2024-11-23&mlyRange=%7C&StationID=51459&Prov=ON&timeframe=2) |

---

## Weather Flag Legend Table

In the `merged_data.csv`, several columns use flags (e.g., `Temp Flag`, `Deg Days Flag`) to denote specific conditions:

| Flag  | Meaning                                                   | Explanation                                                           |
|-------|-----------------------------------------------------------|-----------------------------------------------------------------------|
| A     | Accumulated                                               |                                                                       |
| C     | Precipitation occurred, amount uncertain                 |                                                                       |
| E     | Estimated                                                 |                                                                       |
| F     | Accumulated and estimated                                |                                                                       |
| L     | Precipitation may or may not have occurred               |                                                                       |
| M     | Missing                                                   | Data is unavailable or was not recorded.                             |
| N     | Temperature missing but known to be > 0                  |                                                                       |
| S     | More than one occurrence                                 |                                                                       |
| T     | Trace                                                    | Insignificant precipitation observed, too small to measure.           |
| Y     | Temperature missing but known to be < 0                  |                                                                       |
| [empty] | Unobserved value                                        |                                                                       |
| ^     | Incomplete data                                           |                                                                       |
| †     | Data not reviewed by the National Climate Archives       | Unvalidated data from the National Climate Archives.                 |
