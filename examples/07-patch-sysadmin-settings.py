#!/usr/bin/env python
import elabapi_python

from client import api_client

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
