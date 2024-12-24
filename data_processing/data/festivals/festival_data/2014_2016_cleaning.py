import requests
import json 
import csv
import pandas as pd
import io
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import parse

intermediate = "cleaned_2014_2016.csv"
json_file = "resources_metadata.json"
want = "festivals-and-events-historical-xml-feed-jan-2014-dec-2016"

def downloadXML(json_file, fileWanted):
    with open(json_file, 'r') as file: 
        data = json.load(file)

    # Select the URL corresponding to the requested file
    url = None
    for item in data:
        if item["result"]["name"] == fileWanted:
            url = item["result"]["url"]
            break  # Stop searching once the file is found

    if url is None:
        print(f"File '{fileWanted}' not found in the JSON file.")
        return None

    # Load and parse the XML
    try:
        xml_file = requests.get(url, stream=True)
        xml_file.raise_for_status()  # Raise an error for HTTP issues
        print("URL is valid and accessible.")
        return xml_file.content
    except requests.RequestException as e:
        print(f"Error accessing URL: {e}")
        return None

def xml2CSV(xml_file, intermediate_csv):
    # Parse the XML file
    tree = ET.parse(io.BytesIO(xml_file))
    root = tree.getroot()

    # Extract unique 'name' attributes for specified column range
    headers = []
    for entrydata in root.findall(".//entrydata"):
        columnnumber = entrydata.attrib.get("columnnumber")
        name = entrydata.attrib.get("name")

        if columnnumber is not None and name is not None:
            columnnumber = int(columnnumber)  # Convert to integer for comparison
            if 0 <= columnnumber <= 60 and columnnumber != 4:
                if name not in headers:
                    headers.append(name)

    # Extract data rows
    data_rows = []
    for viewentry in root.findall(".//viewentry"):
        row = []
        for header in headers:
            entrydata = viewentry.find(f".//entrydata[@name='{header}']")
            if entrydata is not None:
                text = entrydata.find("text").text if entrydata.find("text") is not None else ""
                row.append(text)
            else:
                row.append("")  # If no matching entrydata, leave it empty
        if row not in data_rows:
          data_rows.append(row)

    # Write extracted XML data to an intermediate CSV
    with open(intermediate_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)  # Write header row
        writer.writerows(data_rows)  # Write data rows

def main():
    xml2Convert=downloadXML(json_file,want)
    xml2CSV(xml2Convert, intermediate)

if __name__ == "__main__":
    main()