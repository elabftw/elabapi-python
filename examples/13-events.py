#!/usr/bin/env python

###############
# DESCRIPTION #
##############
# In this script, we show how to work with calendar events
##############

# the python library for elabftw
import elabapi_python
from client import api_client

# Load the events api
eventsApi = elabapi_python.EventsApi(api_client)

# get a list of events in the current team
events = eventsApi.read_events()
for event in events:
    print(event)
