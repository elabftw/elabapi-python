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
# Description: patch instance config
####################################

# Load config api
config = elabapi_python.ConfigApi(api_client)

# Create a dictionary with the config we want to modify
# See: https://doc.elabftw.net/api/v2/#/Config/patch-config
params = {
    'admins_create_users': '0',
    'blox_enabled': '0',
    'deletable_xp': '0',
    'lang': 'fr_FR',
    'support_url': 'https://ticket.example.org',
}

# Send the request
config.patch_config(body=params)
