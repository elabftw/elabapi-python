#!/usr/bin/env python

###############
# DESCRIPTION #
###################################################################
# In this script, we will create a resource category and patch it #
###################################################################

import elabapi_python
# random lib to create a random color for our category
import random
from client import api_client

# In this example, categories will be linked to the current team.
TEAM_ID = "current"
# Load the resources categories api
resourcesCategoriesApi = elabapi_python.ResourcesCategoriesApi(api_client)

category = 'category from API'
color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
# create a category with its title and color
response =  resourcesCategoriesApi.post_team_one_rescat_with_http_info(TEAM_ID, body={'title': category, 'color': color})
# the response location for this endpoint is a bit different from the rest:
# the location returns : https://elab.example.org/api/v2/teams/1/items_categories/20
# but the correct url is https://elab.example.org/api/v2/teams/1/resources_categories/20
locationHeaderInResponse = response[2].get('Location')
print(f'The newly created resource category is here: {locationHeaderInResponse}')
category_id = int(locationHeaderInResponse.rstrip('/').split('/')[-1])
print(f"The category's ID is: {category_id}")
# now change the title and color
resourcesCategoriesApi.patch_rescat(TEAM_ID, category_id, body={'title': 'The new title for the category from API', 'color': '#f5c211'})
