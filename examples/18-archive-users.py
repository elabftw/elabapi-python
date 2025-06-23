#!/usr/bin/env python
from datetime import datetime
from dateutil.relativedelta import relativedelta
# the python library for elabftw
import elabapi_python

#####################
#    DESCRIPTION    #
#                   ################################################################################################
# In this script, we look at the last time a user logged in and archive their account after 8 months of inactivity #
# This script would typically be run by an Sysadmin user                                                           #
####################################################################################################################

#########################
#         CONFIG        #
#########################
# replace with the URL of your instance
API_HOST_URL = 'https://elab.local:3148/api/v2'
# replace with your api key
API_KEY = 'apiKey4Test'

# this is the date format we get back from API
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
# we want to archive users not logged in after 8 months
INACTIVE_PERIOD_MONTHS = 8
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
def should_be_archived(date_string):
    date_format = "%Y-%m-%d %H:%M:%S"
    input_date = datetime.strptime(date_string, date_format)
    current_date = datetime.now()
    threshold_date = current_date - relativedelta(months=INACTIVE_PERIOD_MONTHS)
    return input_date < threshold_date

# Load the users api
usersApi = elabapi_python.UsersApi(api_client)

# loop over all users
users = usersApi.read_users()
for user in users:
    # uncomment to print emails and last login time
    # print(f'{user.email}: {user.last_login}')

    # if user never logged in, it'll be NULL in MySQL, so None in python
    # also prevent archival of sysadmin accounts (server will throw error anyway)
    if user.last_login is not None and user.is_sysadmin != 1:
        if should_be_archived(user.last_login):
            print(f'Archiving user {user.email}. Last login: {user.last_login}')
            usersApi.patch_user(user.userid, body={'action': 'archive'})
