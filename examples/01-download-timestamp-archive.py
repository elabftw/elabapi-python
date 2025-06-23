#!/usr/bin/env python
import datetime
import elabapi_python

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

# create an instance of Experiments and another for Uploads
experimentsApi = elabapi_python.ExperimentsApi(api_client)
uploadsApi = elabapi_python.UploadsApi(api_client)

# calculate the date
today = datetime.date.today()
date_from = today - datetime.timedelta(days = PERIOD_IN_DAYS)

# look for experiments that are timestamped
for exp in experimentsApi.read_experiments(extended=f'timestamped:yes timestamped_at:>{date_from}'):
    for upload in uploadsApi.read_uploads('experiments', exp.id):
        # we only look at immutable uploads => timestamp archives
        if upload.immutable:
            now = datetime.datetime.now()
            # get and save binary file
            with open(f'{exp.id}-{exp.elabid}-{now.strftime("%Y-%m-%d_%H-%M-%S")}-timestamp-archive.zip', 'wb') as zipfile:
                # the _preload_content flag is necessary so the api_client doesn't try and deserialize the response
                zipfile.write(uploadsApi.read_upload('experiments', exp.id, upload.id, format='binary', _preload_content=False).data)

