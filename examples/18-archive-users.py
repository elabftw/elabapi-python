#!/usr/bin/env python
from datetime import datetime
from dateutil.relativedelta import relativedelta
# the python library for elabftw
import elabapi_python
from client import api_client

#####################
#    DESCRIPTION    #
#                   ################################################################################################
# In this script, we look at the last time a user logged in and archive their account after 8 months of inactivity #
# This script would typically be run by an Sysadmin user                                                           #
####################################################################################################################

# this is the date format we get back from API
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
# we want to archive users not logged in after 8 months
INACTIVE_PERIOD_MONTHS = 8

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

# TODO: fix last_login info is not provided anymore when user is not admin!
