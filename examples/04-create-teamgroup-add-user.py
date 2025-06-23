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

# Load teamgroup api
teamgroupsApi = elabapi_python.TeamgroupsApi(api_client)

# Create a teamgroup in team with id 1
targetTeam = 1
response = teamgroupsApi.post_teamgroups_with_http_info(targetTeam, body={'name': 'Group name from api'})
# the response is a tuple: (None, 201, HttpHeaderDict)
locationHeaderInResponse = response[2].get('Location')
tgId = int(locationHeaderInResponse.split('/').pop())
# now add user with id 2 to that Group
teamgroupsApi.patch_teamgroup(targetTeam, tgId, body={'how': 'add', 'userid': 2})
