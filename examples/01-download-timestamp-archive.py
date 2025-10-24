#!/usr/bin/env python
import datetime
import elabapi_python
from client import api_client

# define number of days to look back
PERIOD_IN_DAYS = 7

# create an instance of Experiments and another for Uploads
experimentsApi = elabapi_python.ExperimentsApi(api_client)
uploadsApi = elabapi_python.UploadsApi(api_client)

# calculate the date
today = datetime.date.today()
date_from = today - datetime.timedelta(days = PERIOD_IN_DAYS)

# look for experiments that are timestamped
for exp in experimentsApi.read_experiments(extended=f'timestamped:yes timestamped_at:>{date_from}'):
    for upload in uploadsApi.read_uploads('experiments', exp.id, state='1,2'):
        # we only look at immutable uploads => timestamp archives
        if upload.immutable:
            now = datetime.datetime.now()
            # get and save binary file
            with open(f'{exp.id}-{exp.elabid}-{now.strftime("%Y-%m-%d_%H-%M-%S")}-timestamp-archive.zip', 'wb') as zipfile:
                # the _preload_content flag is necessary so the api_client doesn't try and deserialize the response
                zipfile.write(uploadsApi.read_upload('experiments', exp.id, upload.id, format='binary', _preload_content=False).data)

