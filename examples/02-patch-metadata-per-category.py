#!/usr/bin/env python
import elabapi_python

#########################
#         CONFIG        #
#########################
API_HOST_URL = 'https://elab.local:3148/api/v2'
# replace with your api key
API_KEY = 'apiKey4Test'
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

metadata = '{"elabftw": {"extra_fields_groups": [{"id": 1,"name": "Drug settings"},{"id": 2,"name": "Mice info"}]},"extra_fields": {"Drug addition": {"type": "datetime-local","value": "","group_id": 1,"required": true,"description": "Time when drug is added"},"Drug concentration": {"type": "number","unit": "mM","units": ["mM","μM","nM"],"value": "","group_id": 1,"required": true},"Mouse sex": {"type": "select","value": "Male","options": ["Male","Female"],"group_id": 2}}}'

for item in itemsApi.read_items(cat=1, limit=9999):
    # skip items with metadata already
    if not item.metadata:
        print(f'Patching item {item.id}')
        itemsApi.patch_item(item.id, body={'metadata': metadata})

