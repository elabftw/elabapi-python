#!/usr/bin/env python

######################################################################
# In this example script, we show you how to timestamp an experiment #
######################################################################

import elabapi_python
from client import api_client

exp_client = elabapi_python.ExperimentsApi(api_client)

# create an experiment
response_data, status_code, headers = exp_client.post_experiment_with_http_info()
# the Location response header will point to the newly created entry
location = headers.get('Location')
# extract the ID as an integer from the Location string: it is simply the last part of the URL
exp_id = int(location.split('/').pop())
# A status code of 201 means the entry was created
if status_code == 201:
    print(f"[*] We created an experiment. The status code is {status_code} and the experiment is at: {location}")

# now timestamp it
print(exp_id)
exp_client.patch_experiment(exp_id, body={'action': 'timestamp'})
print("Experiment was timestamped")
