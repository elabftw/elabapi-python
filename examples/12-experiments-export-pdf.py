#!/usr/bin/env python
import datetime

###############
# DESCRIPTION #
##############
# In this script, we list experiments from a user and save the recently modified into a PDF
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

#### SCRIPT START ##################

# Load the experiments api
experimentsApi = elabapi_python.ExperimentsApi(api_client)

# calculate the date
today = datetime.date.today()
date_from = today - datetime.timedelta(days = PERIOD_IN_DAYS)

# get a list of experiments for user with ID:2
# OWNER: the target userid. Note: using owner keyword requires elabapi 0.6.0
# LIMIT: the max number of items to return. Use a high limit so we get all at once
# EXTENDED: this is the content of the advanced search, here we filter on timestamped entries during last week
results = experimentsApi.read_experiments(owner=2, limit=9999, extended=f'timestamped:yes timestamped_at:>{date_from}')
for exp in results:
    now = datetime.datetime.now()
    filename = f'{exp.id}-{exp.elabid}-{now.strftime("%Y-%m-%d_%H-%M-%S")}-export.pdf'
    print(f'Saving file {filename}')
    with open(filename, 'wb') as file:
        # the _preload_content flag is necessary so the api_client doesn't try and deserialize the response
        file.write(experimentsApi.get_experiment(exp.id, format='pdf', _preload_content=False).data)
