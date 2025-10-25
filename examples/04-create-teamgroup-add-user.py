#!/usr/bin/env python
import elabapi_python
from client import api_client

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
