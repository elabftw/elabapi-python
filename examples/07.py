#!/usr/bin/env python


import elabapi_python
from elabapi_python.rest import ApiException

#replace with your api key
my_api_key = 'xxxxx'

# Config
configuration = elabapi_python.Configuration()
configuration.api_key['api_key'] = my_api_key
configuration.api_key_prefix['api_key'] = 'Authorization'
configuration.host = 'xxxx'
configuration.debug = True
configuration.verify_ssl = False

# create an instance of the API class
api_client = elabapi_python.ApiClient(configuration)
# fix issue with Authorization header not being properly set by the generated lib
api_client.set_default_header(header_name='Authorization', header_value=my_api_key)

#Create instance of ExperimentTemplateApi
templateApi = elabapi_python.ExperimentsTemplatesApi(api_client)


#Template that we want to create
template_format = {
     'body': '',
     'canread': '{"base": 30, "teams": [], "users": [], "teamgroups": []}',
     'canwrite': '{"base": 20, "teams": [], "users": [], "teamgroups": []}',
     'fullname': 'User 1',
     'is_pinned': 0,
     'locked': 0,
     'lockedby': None,
     'lockedwhen': None,
     'metadata': '{"extra_fields": {"End date": {"type": "date", "value": '
                 '"2021-06-09"}, "Ethical": {"type": "select", "value": '
                 '"123456", "options": ["123456", "20000", "12345"]}, '
                 '"Magnification": {"type": "select", "value": "20X", "options": '
                 '["10X", "20X", "40X"]}}}',
     'tags': None,
     'tags_id': None,
     'teams_id': 21,
     'title': 'Test PATCH',
     'userid': 6
}

#Use of the post funtion to create a new template
res = templateApi.post_experiment_template_with_http_info(body={'title': 'API Creation'})
locationHeaderInResponse = res[2].get('Location')
print(f'The newly created template is here: {locationHeaderInResponse}')
itemId = int(locationHeaderInResponse.split('/').pop())

#Change informations in the template
templateApi.patch_experiment_template(itemId, body={'title': 'Test'})
