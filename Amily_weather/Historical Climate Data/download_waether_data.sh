# Define an associative array with station names and IDs
declare -A stations
stations=(
  ["TORONTO_CITY"]="31688"
  ["TORONTO_CITY_CENTRE"]="48549"
  ["TORONTO_NORTH_YORK"]="26953"
  ["TORONTO_INTL_A"]="51459"
)

# Base download folder
base_folder="./"  # Replace with your desired base folder
mkdir -p "$base_folder"

# Loop through each station
for station in "${!stations[@]}"; do
  stationID=${stations[$station]}
  
  # Create a folder for the current station
  station_folder="$base_folder/$station"
  mkdir -p "$station_folder"
  
  # Loop through years and months to download data
  for year in `seq 2014 2024`; do
    for month in `seq 1 12`; do
      wget --content-disposition -P "$station_folder" "https://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID=${stationID}&Year=${year}&Month=${month}&Day=14&timeframe=2&submit=Download+Data"
    done
  done
done
