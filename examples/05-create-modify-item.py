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

# Load items api
itemsApi = elabapi_python.ItemsApi(api_client)

# Create an item with the category_id 1 (items_types ID = 1)
targetCategory = 1
response = itemsApi.post_item_with_http_info(body={'category_id': targetCategory, 'tags': ['some tag', 'another tag']})
locationHeaderInResponse = response[2].get('Location')
print(f'The newly created item is here: {locationHeaderInResponse}')
itemId = int(locationHeaderInResponse.split('/').pop())
# now change the title, and body and rating
itemsApi.patch_item(itemId, body={'title': 'The new title', 'body': 'Main content text', 'rating': 5})
