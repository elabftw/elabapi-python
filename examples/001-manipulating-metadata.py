#!/usr/bin/env python

###################################################################################################
# In this example script, we show you how to manage extra fields through the "metadata" attribute #
###################################################################################################

from pprint import pprint
import elabapi_python

# use the locally defined client.py module to get the api_client object, fully configured and ready to be used to instantiate api objects
from client import api_client

# Note:
# In order to make it easier to run only specific parts, the parts are grouped in functions that are called at the end of the script

######################################################
# Part 1: creating a Resource with specific metadata #
######################################################
# Doc: https://doc.elabftw.net/api/v2/#/Items/post-item
# Start by creating our api object to interact with /items endpoint
items_client = elabapi_python.ItemsApi(api_client)

# Now define our metadata: in this case, two fields of type number, with units
metadata = {
    "extra_fields": {
        "Laser power": {
            "type": "number",
            "value": "50",
            "units": ["mW", "W", "MW"],
            "unit": "MW",
        },
        "Illumination time": {
            "type": "number",
            "value": "85",
            "units": ["min", "sec", "hour"],
            "unit": "min",
        },
    },
}

# now create a Resource with this metadata
data = {
    "title": "Resource with metadata created from API",
    "metadata": metadata,
}
response_data, status_code, headers = items_client.post_item_with_http_info(body=data)
item_id = int(headers.get('Location').split('/').pop())
if status_code == 201:
    print(f"[*] We created a Resource with ID: {item_id}")
