#!/usr/bin/env python
import os
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

# create an instance of Experiments and another for Uploads
experimentsApi = elabapi_python.ExperimentsApi(api_client)
uploadsApi = elabapi_python.UploadsApi(api_client)

# get experiment with ID 256
exp = experimentsApi.get_experiment(256)
# upload the file 'README.md' present in the current folder
uploadsApi.post_upload('experiments', 256, file='README.md', comment='Uploaded with APIv2')
# display id, name and comment of the uploaded files
for upload in uploadsApi.read_uploads('experiments', exp.id):
    print(upload.id, upload.real_name, upload.comment)
    # get and save file
    with open('README.downloaded_with_api.md', 'wb') as file:
        # the _preload_content flag is necessary so the api_client doesn't try and deserialize the response
        file.write(uploadsApi.read_upload('experiments', 256, upload.id, format='binary', _preload_content=False).data)
    # delete all the files where the name is 'README.md'
    if upload.real_name == 'README.md':
        uploadsApi.delete_upload('experiments', 256, upload.id)

# cleanup: delete the downloaded file
os.remove('README.downloaded_with_api.md')
