#!/usr/bin/env python

###################################################################
# In this example script, we create a link to a resource          #
# We want to link the resource with ID 12 to experiment with id 6 #
###################################################################

import elabapi_python

# use the locally defined client.py module to get the api_client object, fully configured and ready to be used to instantiate api objects
from client import api_client

links_api = elabapi_python.LinksToItemsApi(api_client)

experiment_id = 6
resource_id = 12

links_api.post_entity_items_links('experiments', experiment_id, resource_id)
