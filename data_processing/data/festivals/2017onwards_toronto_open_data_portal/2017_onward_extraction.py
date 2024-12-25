import requests
import json
import pandas as pd

data_month = 'Sep'

data_year = "2019"

previous_month = 'Sep'

previous_year = '2019'

new_json_name = f"{data_year}{data_month}.json"

#the url which is valid on Wayback Machine  for downloading past json calendar feed
url = "https://web.archive.org/web/20190930151814/http://app.toronto.ca:80/cc_sr_v1_app/data/edc_eventcal_APR"

def downloadJSON(url_past):
    try:
        feed_file = requests.get(url_past, stream=True)
        feed_file.raise_for_status()  # Raise an error for HTTP issues
        print("URL is valid and accessible.")
        # Write the content to a local file
        with open(new_json_name, "wb") as file:
            for chunk in feed_file.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)

        print(f"File downloaded successfully as {new_json_name}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def main():
    downloadJSON(url)

if __name__ == "__main__":
    main()
        
