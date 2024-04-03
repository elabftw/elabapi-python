#!/usr/bin/env python
import datetime

###############
# DESCRIPTION #
##############
# In this script, we show how to work with calendar events
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

# Load the events api
eventsApi = elabapi_python.EventsApi(api_client)

# get a list of events in the current team
events = eventsApi.read_events()
for event in events:
    print(event)
