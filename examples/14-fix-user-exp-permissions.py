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
from client import api_client

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
