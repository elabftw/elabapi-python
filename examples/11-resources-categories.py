#!/usr/bin/env python

###############
# DESCRIPTION #
##############
# In this script, we will create a resource category and patch it
##############

# the python library for elabftw
import elabapi_python

#########################
#         CONFIG        #
#########################
# replace with the URL of your instance
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

#### SCRIPT START ##################

# Load the items types api
itemsTypesApi = elabapi_python.ItemsTypesApi(api_client)

# create one, we provide a title on creation but it's not mandatory
response = itemsTypesApi.post_items_types_with_http_info(body={'title': "My freshly created category"})
# the response location for this endpoint is a bit different from the rest, it is the full URL: https://elab.example.org/api/v2/items_types/admin.php?tab=4&templateid=15
locationHeaderInResponse = response[2].get('Location')
print(f'The newly created resource category is here: {locationHeaderInResponse}')
itemId = int(locationHeaderInResponse.split('=').pop())
# now change the title, and body and color
itemsTypesApi.patch_items_type(itemId, body={'title': 'The new title', 'body': 'Main content text', 'color': '#f5c211'})
