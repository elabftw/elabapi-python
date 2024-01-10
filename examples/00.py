#!/usr/bin/env python
import time
import json
import elabapi_python
from elabapi_python.rest import ApiException

# replace with your api key
my_api_key = 'apiKey4Test'

# START CONFIG
configuration = elabapi_python.Configuration()
configuration.api_key['api_key'] = my_api_key
configuration.api_key_prefix['api_key'] = 'Authorization'
configuration.host = 'https://elab.local:3148/api/v2'
configuration.debug = False
configuration.verify_ssl = False

# create an instance of the API class
api_client = elabapi_python.ApiClient(configuration)
# fix issue with Authorization header not being properly set by the generated lib
api_client.set_default_header(header_name='Authorization', header_value=my_api_key)
# END CONFIG

# create an instance of Items
items = elabapi_python.ItemsApi(api_client)

# display items with default settings
itemsList = items.read_items()
print(type(itemsList)) # <-- python list
print(itemsList)

# fetch 50 items with a category id of 8
itemsList = items.read_items(limit=50, cat=8)
print(f'Number of results: {len(itemsList)}')

# if you want raw json, use _preload_content=False
# get the response object directly
response = items.read_items(_preload_content=False)
print(response.data.decode('utf-8')) # <-- JSON string
# transform it into python object from JSON
data = response.json()
# and pretty print the firt three elements in JSON
print(json.dumps(data[0:3], indent=2))
