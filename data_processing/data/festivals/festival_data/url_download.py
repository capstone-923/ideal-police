import requests
import json

# Toronto Open Data is stored in a CKAN instance. It's APIs are documented here:
# https://docs.ckan.org/en/latest/api/

# To hit the Toronto Open Data API, you'll be making requests to:
base_url = "https://ckan0.cf.opendata.inter.prod-toronto.ca"

# Datasets are called "packages". Each package can contain many "resources"
# To retrieve the metadata for this package and its resources, use the package name in this page's URL:
url = base_url + "/api/3/action/package_show"
params = { "id": "festivals-events"}
package = requests.get(url, params = params).json()
print("Package structure: ", package)
resources_metadata = []

# To get resource data:
for idx, resource in enumerate(package["result"]["resources"]):

       # To get metadata for non datastore_active resources:
       if not resource["datastore_active"]:
           url = base_url + "/api/3/action/resource_show?id=" + resource["id"]
           resource_metadata = requests.get(url).json()
           resources_metadata.append(resource_metadata)
           # From here, you can use the "url" attribute to download this file

           #store all the urls from the listed three subsets to a list/dictionary
           #we are going to use the first subset because that contain festivals from 2016-2024 and is still being updated.
           #the second dataset is a readme; the third on is 2014-2016 xml dataset.

# Save all_resources_metadata to a JSON file
with open("resources_metadata.json", "w") as f:
    json.dump(resources_metadata, f, indent=4)

print("Resource metadata saved to resources_metadata.json")



