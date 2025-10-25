#!/usr/bin/env python
import datetime

###############
# DESCRIPTION #
##############
# In this script, we list experiments from a user and save the recently modified into a PDF
##############

# the python library for elabftw
import elabapi_python
from client import api_client

PERIOD_IN_DAYS = 7

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
