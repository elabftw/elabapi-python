#!/usr/bin/env python

###############
# DESCRIPTION #
##############
# In this script, we will work with date-time data by doing statistics with experiments. Date-time information returned
# by elabapi-python are in string formats, and we would like to convert the strings to a workable format,
# so we can programmatically manipulate them for later use.
##############

# necessary imports for this example
# datetime module for converting strings to datetime instances
from datetime import datetime

# the python library for elabftw
import elabapi_python
# Pandas library for converting dictionary to dataframe (plotting tools like seaborn knows how to plot dataframes)
import pandas as pd
# Seaborn to plot the dataframe from pandas
import seaborn as sns

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

# Load the experiments api
experiments = elabapi_python.ExperimentsApi(api_client)

# We would like to see the frequency of experiment creation over the past years. First we need to be able to parse the
# date-time value from "created_at" field. For that we structure the data first.
data = experiments.read_experiments()

# We can try looking at one of the dates to see if it worked.
print(data[0].created_at)
# The datetime is in string format (ISO 8601). Though some libraries already know how to handle date-time data that are
# in string format by implicitly converting them to Python datetime objects. Here we will do the conversion ourselves.
# Let's take a look at how that would look like.
print(datetime.fromisoformat(data[0].created_at))  # strips date-time in ISO 8601.
# For working with date-time **programmatically** you want to work with this datetime instance
# instead of the string format everywhere.
print(
    datetime.fromisoformat(data[0].created_at).strftime("%Y")
)  # only gives the year value
# Now we collect all the "created_at" dates.
created_at = [datetime.fromisoformat(time.created_at).strftime("%Y") for time in data]
# An alternative of fromisoformat() would be strptime("%m-%d-%Y %H:%M:%S", time.created_at). If we wanted to get months
# instead of years we would use strftime("%m"). Have a look at this wonderful reference site for all sorts
# date-time formats: https://strftime.org/.
# For things like parsing timezones and other date-time paring related information,
# please refer to the official documentation of datetime: https://docs.python.org/3/library/datetime.html

# To make our final plot interesting we would like to see how the frequency looks like when it is color encoded (hue)
# with "status". I.e., we would expect the older an experiment is the more likely its status is set to "Success".
# Status by default is assigned "Running".
status = [s.category for s in data]  # In the API response "status" is named "category"

# Though we won't plot the experiments IDs, just for future reference we collect the IDs as well.
ids = [i.id for i in data]

# Now we create the Pandas dataframe for plotting
plot_data = {
    "Experiment IDs": created_at,
    "Creation Year": created_at,
    "Status": status,
}
df = pd.DataFrame.from_dict(plot_data)
# Now we plot.
sns.countplot(data=df, x="Creation Year", hue="Status")
# And that should give us an interesting discrete time series plot!
