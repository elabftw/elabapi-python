#!/usr/bin/env python
import time
import datetime
import elabapi_python
from elabapi_python.rest import ApiException

#########################
#         CONFIG        #
#########################
API_HOST_URL = 'https://elab.local:3148/api/v2'
# replace with your api key
API_KEY = 'apiKey4Test'
# number of days to look back
PERIOD_IN_DAYS = 7
#########################
#      END CONFIG       #
#########################

# Configure the api client
configuration = elabapi_python.Configuration()
configuration.api_key['api_key'] = API_KEY
configuration.api_key_prefix['api_key'] = 'Authorization'
configuration.host = API_HOST_URL
configuration.debug = False
configuration.verify_ssl = False

# create an instance of the API class
api_client = elabapi_python.ApiClient(configuration)
# fix issue with Authorization header not being properly set by the generated lib
api_client.set_default_header(header_name='Authorization', header_value=API_KEY)

# Synchronize metadata of the item_type with existing items
# See: https://github.com/elabftw/elabftw/issues/3524

# create an instance of Items api
itemsApi = elabapi_python.ItemsApi(api_client)

for item in itemsApi.read_items(cat=9):
    # skip items with metadata already
    if not item.metadata:
        print(f'Patching item {item.id}')
        itemsApi.patch_item(item.id, body={'metadata': '{"new":"metadata"}'})

