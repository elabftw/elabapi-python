#!/usr/bin/env python
import elabapi_python

# necessary imports for this example
import csv
import json

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
# Description: read a csv file
# and create an item for each row, linked to a project
####################################

# Load the items api
itemsApi = elabapi_python.ItemsApi(api_client)
# and the links too
linksApi = elabapi_python.LinksToItemsApi(api_client)

# this is the path to the CSV file that we will read
csv_path = 'data/samples.csv'

# in which category (items_types) our samples will be created
# this corresponds to the previously created "Samples" category in our database
category_id = 1

# project map (see comment below when linking to a project)
project_map = {'Changes in a child’s subgingival microbiome following prophylaxis': 17, 'Another project': 16}

# this is our metadata json, with an empty value for now, as it will change for every row
# here the main body is hidden with display_main_text: false
base_json='{"extra_fields":{"Sample type":{"type":"select","value":"","options":["Saliva","Tongue","Nose"],"group_id":null,"description":"The type of the sample"}},"elabftw":{"display_main_text": false}}'
# we load it as an object
metadata_as_json = json.loads(base_json)
# read the csv and loop over rows
with open(csv_path, newline='') as csvfile:
    csvreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    for row in csvreader:
        # create an item in the correct category, we also add a tag with the sample_type here
        response = itemsApi.post_item_with_http_info(body={'category_id': category_id, 'tags': [row['sample_type']]})
        # the previous request gives us the ID of the newly created item, so look into the Location header to get it
        locationHeaderInResponse = response[2].get('Location')
        print(f'The newly created item is here: {locationHeaderInResponse}')
        itemId = int(locationHeaderInResponse.split('/').pop())
        # replace the value of the Sample type in metadata with the sample_type of the row
        metadata_as_json['extra_fields']['Sample type']['value'] = row['sample_type']
        # and now we modify the item with the correct title/metadata
        itemsApi.patch_item(itemId, body={'title': row['sample_name'], 'body': '', 'metadata': json.dumps(metadata_as_json)})

        # now we want to link our entry to the project
        # one option would be to GET all items of a particular category and look for the title of our project to get its ID
        # but we will instead use a map because we don't have too many projects and they will never change their ID
        project_id = project_map[row['project_name']]
        linksApi.post_entity_items_links('items', itemId, project_id)
