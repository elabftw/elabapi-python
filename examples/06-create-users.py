#!/usr/bin/env python
import elabapi_python

#########################
#         CONFIG        #
#########################
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

#### SCRIPT START #####
# Description: create users in batch
#######################

# Load users api
users = elabapi_python.UsersApi(api_client)

# the default team in which we want to create the users
# if this parameter is not passed, it will be the team in which the api key in use has been created
default_team = 1

# A list of dictionaries holding the users we wish to create.
users_to_create = [
    {'firstname': 'John', 'lastname': 'Rambo', 'email': 'john.rambo@example.com', 'team': 2},
    {'firstname': 'Nicolas', 'lastname': 'Tesla', 'email': 'nico@tesla.eu', 'team': default_team},
    {'firstname': 'Arthur', 'lastname': 'Martin', 'email': 'tutur@martin.fr', 'team': 3},
    # This user will end up in the team where the api key has been created
    {'firstname': 'Michael', 'lastname': 'Jordan', 'email': 'mike@air.com'},
]

# now loop over the list and create users
for user in users_to_create:
    # create the user by passing directly the dict in the body
    response = users.post_user_with_http_info(body=user)
    # look for the userid in the Location response header
    locationHeaderInResponse = response[2].get('Location')
    userid = int(locationHeaderInResponse.split('/').pop())
    print(f'Created user with id: {userid} in team: {user.get("team", default_team)}.')

print('--------------')
print('Now add user with id 1 to team 3')
users.patch_user(1, body={'action': 'add', 'team': 3})
