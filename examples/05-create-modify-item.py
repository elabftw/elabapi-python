#!/usr/bin/env python
import elabapi_python
from client import api_client

# Load items api
itemsApi = elabapi_python.ItemsApi(api_client)

# Create an item with the category_id 1 (items_types ID = 1)
targetCategory = 1
response = itemsApi.post_item_with_http_info(body={'category': targetCategory, 'tags': ['some tag', 'another tag']})
locationHeaderInResponse = response[2].get('Location')
print(f'The newly created item is here: {locationHeaderInResponse}')
itemId = int(locationHeaderInResponse.split('/').pop())
# now change the title, and body and rating
itemsApi.patch_item(itemId, body={'title': 'The new title', 'body': 'Main content text', 'rating': 5})
