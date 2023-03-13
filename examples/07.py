#!/usr/bin/env python
import time
import datetime
import elabapi_python
from elabapi_python.rest import ApiException

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

# Create instance of ExperimentTemplateApi
templateApi = elabapi_python.ExperimentsTemplatesApi(api_client)


# Template that we want to create, exemple with extra fields
template_format = {
     'metadata': '{"extra_fields": {"End date": {"type": "date", "value": '
                 '"2021-06-09"}, "Ethical": {"type": "select", "value": '
                 '"123456", "options": ["123456", "20000", "12345"]}, '
                 '"Magnification": {"type": "select", "value": "20X", "options": '
                 '["10X", "20X", "40X"]}}}',
}

# Use of the post funtion to create a new template
res = templateApi.post_experiment_template_with_http_info(body={'title': 'API Creation'})
locationHeaderInResponse = res[2].get('Location')
print(f'The newly created template is here: {locationHeaderInResponse}')
itemId = int(locationHeaderInResponse.split('/').pop())

# Change metadata of the template
templateApi.patch_experiment_template(itemId, body={'metadata': template_format['metadata']})
