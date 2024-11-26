## Folder Structure and Contents

### **1. Official Metadata**
This folder contains official documents from the Government of Toronto, providing guidance on downloading historical climate data and details about weather stations.

### **2. Climate Stations**
The repository includes data from **all Toronto weather stations** that have **daily** data available from **2010 to the most up-to-date records (2024)**. The following four key stations are highlighted and included:
- **TORONTO_CITY**
- **TORONTO_CITY_CENTRE**
- **TORONTO_INTL_A**
- **TORONTO_NORTH_YORK**

Each station folder is organized into the following subfolders:
- **Merged**: 
  - `merged_data.csv`
- **Cleaned**: contains some processed data  
  - `basic_clean_data.csv`
  - `basic_clean_data_report.csv`

### **3. Script**
- `download_weather_data.sh`: A shell script for downloading the data for the four climate stations via Cygwin.

## Dataset Information
**Dataset Range**: 2010-01-01 to 2024-12-31  
**Note**: The latest data is updated to 2024-11-17 or 2024-11-24, depending on the station. Data for the remaining time periods is currently unavailable.

## Stations Table

| Station              | Climate ID | Station ID | Link  |
|----------------------|------------|------------|-------|
| TORONTO CITY         | 6158355    | 31688      | [link](https://climate.weather.gc.ca/climate_data/daily_data_e.html?hlyRange=2002-06-04%7C2024-11-23&dlyRange=2002-06-04%7C2024-11-23&mlyRange=2003-07-01%7C2006-12-01&StationID=31688&Prov=ON&urlExtension=_e.html&searchType=stnProx&optLimit=yearRange&Month=11&Day=24&StartYear=2014&EndYear=2024&Year=2024&selRowPerPage=25&Line=2&txtRadius=25&optProxType=city&selCity=43%7C39%7C79%7C23%7CToronto&selPark=&txtCentralLatDeg=&txtCentralLatMin=0&txtCentralLatSec=0&txtCentralLongDeg=&txtCentralLongMin=0&txtCentralLongSec=0&txtLatDecDeg=&txtLongDecDeg=&timeframe=2) |
| TORONTO CITY CENTRE  | 6158359    | 48549      | [link](https://climate.weather.gc.ca/climate_data/daily_data_e.html?hlyRange=2009-12-10%7C2024-11-23&dlyRange=2010-02-02%7C2024-11-23&mlyRange=%7C&StationID=48549&Prov=ON&urlExtension=_e.html&searchType=stnProx&optLimit=yearRange&Month=11&Day=24&StartYear=2014&EndYear=2024&Year=2024&selRowPerPage=25&Line=5&txtRadius=25&optProxType=city&selCity=43%7C39%7C79%7C23%7CToronto&selPark=&txtCentralLatDeg=&txtCentralLatMin=0&txtCentralLatSec=0&txtCentralLongDeg=&txtCentralLongMin=0&txtCentralLongSec=0&txtLatDecDeg=&txtLongDecDeg=&timeframe=2) |
| TORONTO NORTH YORK   | 615S001    | 26953      | [link](https://climate.weather.gc.ca/climate_data/daily_data_e.html?hlyRange=%7C&dlyRange=1994-11-01%7C2024-11-17&mlyRange=1994-01-01%7C2006-12-01&StationID=26953&Prov=ON&urlExtension=_e.html&searchType=stnProx&optLimit=yearRange&Month=11&Day=24&StartYear=2014&EndYear=2024&Year=2024&selRowPerPage=25&Line=14&txtRadius=25&optProxType=city&selCity=43%7C39%7C79%7C23%7CToronto&selPark=&txtCentralLatDeg=&txtCentralLatMin=0&txtCentralLatSec=0&txtCentralLongDeg=&txtCentralLongMin=0&txtCentralLongSec=0&txtLatDecDeg=&txtLongDecDeg=&timeframe=2) |
| TORONTO INTL A       | 6158731    | 51459      | [link](https://climate.weather.gc.ca/climate_data/daily_data_e.html?hlyRange=2013-06-11%7C2024-11-23&dlyRange=2013-06-13%7C2024-11-23&mlyRange=%7C&StationID=51459&Prov=ON&urlExtension=_e.html&searchType=stnProx&optLimit=yearRange&Month=11&Day=24&StartYear=2014&EndYear=2024&Year=2024&selRowPerPage=25&Line=18&txtRadius=25&optProxType=city&selCity=43%7C39%7C79%7C23%7CToronto&selPark=&txtCentralLatDeg=&txtCentralLatMin=0&txtCentralLatSec=0&txtCentralLongDeg=&txtCentralLongMin=0&txtCentralLongSec=0&txtLatDecDeg=&txtLongDecDeg=&timeframe=2) |

---

## Legend Table

| Legend | Official Meaning                                       | Explanation                                                           |
|--------|-------------------------------------------------------|-----------------------------------------------------------------------|
| A      | Accumulated                                           |                                                                       |
| C      | Precipitation occurred, amount uncertain             |                                                                       |
| E      | Estimated                                             |                                                                       |
| F      | Accumulated and estimated                            |                                                                       |
| L      | Precipitation may or may not have occurred           |                                                                       |
| M      | Missing                                               | Data is unavailable or was not recorded.                             |
| N      | Temperature missing but known to be > 0              |                                                                       |
| S      | More than one occurrence                             |                                                                       |
| T      | Trace                                                | An insignificant amount of precipitation was observed, too small to be measured. |
| Y      | Temperature missing but known to be < 0              |                                                                       |
| [empty]| Indicates an unobserved value                        |                                                                       |
| ^      | The value displayed is based on incomplete data      |                                                                       |
| †      | Data that is not subject to review by the National Climate Archives | The data has not been formally reviewed or validated by the National Climate Archives. |

---

## Weather Features

The following headers were removed from the dataset:

These fields are not needed for the analysis:
- `Longitude (x)`
- `Latitude (y)`
- `Climate ID`
- `Date/Time`

These fields are not related to crime rates:
- `Dir of Max Gust (10s deg)`
- `Dir of Max Gust Flag`
- `Spd of Max Gust (km/h)`
- `Spd of Max Gust Flag`
- `Heat Deg Days (°C)`
- `Heat Deg Days Flag`
- `Cool Deg Days (°C)`
- `Cool Deg Days Flag`

