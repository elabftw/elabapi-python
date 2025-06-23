#!/usr/bin/env python
import json

###############
# DESCRIPTION #
##############
# In this script, we get all the experiments of a given user, and set the visibility (canread) and edition (canwrite) permissions to:
# Base: only owner and admin + team group 2
# This script would typically be run by an Admin user
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
# Load the experiments api
experimentsApi = elabapi_python.ExperimentsApi(api_client)

# all experiments belonging to that user will get modified
target_userid = 2
# make sure this team group exists!
# to get its id go to /api/v2/teams/current/teamgroups
target_teamgroup = 2

# This is the permission setting we will assign to the experiments
# base:20 means "User + Admin" (see https://github.com/elabftw/elabftw/blob/b193d9fc738ab2635e07317ad83f8c5c1c50413a/src/enums/BasePermissions.php#L17)
canwrite = canread = { 'base': 20, 'teams': [], 'teamgroups': [target_teamgroup], 'users': [] }

# get a list of experiments for a given user
experiments = experimentsApi.read_experiments(owner=target_userid,limit=9999)
for exp in experiments:
    experimentsApi.patch_experiment(exp.id, body={'canread': json.dumps(canread), 'canwrite': json.dumps(canwrite)})
