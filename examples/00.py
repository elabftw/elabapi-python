#!/usr/bin/env python
import time
import elabapi_python
from elabapi_python.rest import ApiException

# replace with your api key
my_api_key = 'apiKey4Test'

# Config
configuration = elabapi_python.Configuration()
configuration.api_key['api_key'] = my_api_key
configuration.api_key_prefix['api_key'] = 'Authorization'
configuration.host = 'https://elab.local:3148/api/v2'
configuration.debug = True
configuration.verify_ssl = False

# create an instance of the API class
api_client = elabapi_python.ApiClient(configuration)
# fix issue with Authorization header not being properly set by the generated lib
api_client.set_default_header(header_name='Authorization', header_value=my_api_key)

# create an instance of Items
items = elabapi_python.ItemsApi(api_client)
# display items with default settings
print(items.read_items())
# display 50 items with a category id of 8
print(len(items.read_items(limit=50, cat=8)))
