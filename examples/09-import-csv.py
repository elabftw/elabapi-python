#!/usr/bin/env python

###############
# DESCRIPTION #
##############
#
# This script will read a csv file that contains a list of antibodies, and add
# them to the resources database with a fine control on which columns are
# processed and how.
#

# the python lib for elab
import elabapi_python
# we will use the generic csv module
import csv
# we also need the json module for the metadata (extra fields) part
import json

#########################
#         CONFIG        #
#########################
# replace with your instance address
API_HOST_URL = 'https://elab.local:3148/api/v2'
# replace with your api key
API_KEY = 'apiKey4Test'
# this is the resource category where the entries will be created. Visit /api/v2/items_types to GET a list.
# in this example, category with id 6 corresponds to "Antibody"
RESOURCE_CATEGORY_ID = 6
# path to the csv file, change this too
CSV_PATH = './data/antibodies.csv'
#########################
#      END CONFIG       #
#########################

# Configure the api client
configuration = elabapi_python.Configuration()
configuration.api_key['api_key'] = API_KEY
configuration.api_key_prefix['api_key'] = 'Authorization'
configuration.host = API_HOST_URL
configuration.debug = False
# set to True if you have a proper certificate, here it is set to False to ease the test in dev
configuration.verify_ssl = False

# create an instance of the API class
api_client = elabapi_python.ApiClient(configuration)
# fix issue with Authorization header not being properly set by the generated lib
api_client.set_default_header(header_name='Authorization', header_value=API_KEY)

# Load items api
itemsApi = elabapi_python.ItemsApi(api_client)

# REAL STUFF STARTS HERE

# function to build the metadata json for a row
def getMetadataFromRow(row):
    # our metadata object for one row, currently a dictionary with a key "extra_fields" holding an empty dictionary
    metadata = { 'extra_fields': {} }
    # now go over the columns (except the title/Name) and add it to our extra_fields object
    for keyval in row.items():
        field_type = 'text'
        # we don't import these columns as metadata
        # Name is the tile, Comment is in the body, and ID is the custom_id.
        if keyval[0] == 'Name' or keyval[0] == 'Comment' or keyval[0] == 'ID':
            continue
        # special case for url/URL column, we make it a type: url
        if keyval[0].lower() == 'url':
            field_type = 'url'
        if keyval[0].lower() == 'price':
            field_type = 'number'
        # special case for Concentration column, we use the units
        if keyval[0].lower() == 'concentration' and keyval[1]:
            split_conc = keyval[1].split()
            metadata['extra_fields'].update({keyval[0]: {'value': split_conc[0], 'type': 'number', 'unit': split_conc[1], 'units':['mg/mL', 'μg/mL']}})
        elif keyval[0].lower() == 'primary vs secondary':
            metadata['extra_fields'].update({keyval[0]: {'value': 'Primary', 'type': 'select', 'options': ['Primary', 'Secondary']}})

        elif keyval[0].lower() == 'raised in':
            metadata['extra_fields'].update({keyval[0]: {'value': keyval[1], 'type': 'select', 'options': ['Rabbit', 'Mouse']}})
        elif keyval[0].lower() == 'recognizes':
            metadata['extra_fields'].update({keyval[0]: {
                'value': keyval[1].split(', '), 'type': 'select', 'allow_multi_values': True, 'options': ['Ape', 'Chicken', 'Dog', 'Goat', 'Guinea Pig', 'Hamster', 'Human', 'Mink', 'Monkey', 'Mouse', 'Rabbit', 'Rat', 'Sheep', 'Zebrafish']}})
        else:
            metadata['extra_fields'].update({keyval[0]: {'value': keyval[1], 'type': field_type}})
    return json.dumps(metadata)

# The column "Comment" will get added to the body of the resource
def getBodyFromRow(row) -> str:
    for keyval in row.items():
        if keyval[0] == 'Comment':
            return f'<p>{keyval[1]}</p>'
    return ''

###########################################
######## WHERE THE MAGIC HAPPENS ##########
###########################################

# Note: use encoding='utf-8-sig' in the open() call if your file has BOM (Byte Order Mark)
# Also make sure that the CSV file was saved as UTF-8 to avoid issues with special characters
with open(CSV_PATH, newline='') as csvfile:
    # let's read the CSV using the standard "csv" library from python. No need for anything fancier.
    csvreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    # now we loop over each row in our CSV
    for row in csvreader:
        # here we add the tag "-20°C freezer" to every row
        # the API allows setting tags during creation (POST) of a resource or experiment, so we use it here
        response = itemsApi.post_item_with_http_info(body={'category_id': RESOURCE_CATEGORY_ID, 'tags': ['-20°C freezer']})
        locationHeaderInResponse = response[2].get('Location')
        # that's our ID of the newly created resource
        itemId = int(locationHeaderInResponse.split('/').pop())

        # Patch the item to change its content:
        # the "Name" column becomes our title
        # the "Body" is generated from the "Comment" column content with the "getBodyFromRow()" function
        # for the "ID" column we match it to the "custom_id" property in elab
        # and the extra fields (metadata) is built with a function
        # the single line below will make all those changes at once
        itemsApi.patch_item(itemId, body={'title': row['Name'], 'body': getBodyFromRow(row), 'custom_id': row['ID'], 'metadata': getMetadataFromRow(row)})
